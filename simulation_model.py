import simpy
import random
import numpy as np

# Simulation Core Components
class Metrics:
    """Class that store simulation results."""
    def __init__(self):
        self.wait_times = []
        self.turnaround_times = []
        self.queue_over_time = []
        self.queue_timestamps = []
        self.total_service_time = 0
        self.tasks_completed = 0

def task(env, name, scheduler, metrics, avg_service_time, service_std_dev):
    """
    SimPy process representing a single task.
    It arrives, requests a thread, executes, and leaves.
    """
    arrival_time = env.now

    # Request a thread from the scheduler
    with scheduler.request() as req:
        yield req
        
        # Got a thread, record wait time
        execution_start_time = env.now
        wait_time = execution_start_time - arrival_time
        metrics.wait_times.append(wait_time)

        # Simulate task execution (service)
        # Service time is drawn from a normal distribution
        service_time = random.normalvariate(avg_service_time, service_std_dev)
        # Ensure service time is not negative or zero
        service_time = max(0.1, service_time) 
        
        yield env.timeout(service_time)
        
        # Task complete, record metrics
        completion_time = env.now
        turnaround_time = completion_time - arrival_time
        
        metrics.turnaround_times.append(turnaround_time)
        metrics.total_service_time += service_time
        metrics.tasks_completed += 1

def task_generator(env, scheduler, metrics, arrival_rate, avg_service_time, service_std_dev):
    """
    SimPy process that generates new tasks based on an exponential
    inter-arrival time (Poisson process).
    """
    task_id = 0
    while True:
        # Wait for the next task arrival
        # Inter-arrival time is from an exponential distribution
        inter_arrival_time = random.expovariate(arrival_rate)
        yield env.timeout(inter_arrival_time)
        
        # Create and start the new task process
        task_id += 1
        env.process(task(env, f'Task-{task_id}', scheduler, metrics, 
                         avg_service_time, service_std_dev))

def queue_monitor(env, scheduler, metrics):
    """
    SimPy process that periodically samples the length
    of the scheduler's queue.
    """
    while True:
        metrics.queue_timestamps.append(env.now)
        metrics.queue_over_time.append(len(scheduler.queue))
        yield env.timeout(1.0) # Sample every 1.0 time unit

# Simulation Runner
def run_simulation(num_threads, arrival_rate, avg_service_time, sim_time):
    """
    Sets up and runs a single simulation scenario.
    Returns a dictionary of summary statistics and the raw metrics object.
    """
    # Initialize metrics and SimPy environment
    metrics = Metrics()
    env = simpy.Environment()
    
    # Create the scheduler resource (thread pool)
    scheduler = simpy.Resource(env, capacity=num_threads)
    
    # Set the standard deviation of service time (e.g., 10% of the mean)
    service_std_dev = avg_service_time * 0.1
    
    # Start the processes
    env.process(task_generator(env, scheduler, metrics, arrival_rate, 
                               avg_service_time, service_std_dev))
    env.process(queue_monitor(env, scheduler, metrics))
    
    # Run the simulation
    env.run(until=sim_time)
    
    # Calculate summary statistics
    if not metrics.wait_times: # Handle case with zero tasks
        return {'avg_wait': 0, 'avg_turnaround': 0, 'avg_queue': 0, 
                'utilization': 0, 'tasks_completed': 0}, metrics

    avg_wait = np.mean(metrics.wait_times)
    avg_turnaround = np.mean(metrics.turnaround_times)
    avg_queue = np.mean(metrics.queue_over_time)
    
    # Calculate utilization
    total_available_time = num_threads * sim_time
    utilization = (metrics.total_service_time / total_available_time) * 100
    
    summary = {
        'avg_wait': round(avg_wait, 2),
        'avg_turnaround': round(avg_turnaround, 2),
        'avg_queue': round(avg_queue, 2),
        'utilization': round(utilization, 1),
        'tasks_completed': metrics.tasks_completed
    }
    
    return summary, metrics
