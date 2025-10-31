import json
import pandas as pd
import random
import numpy as np
import os
import re

# Import modules
from simulation_model import run_simulation
from plotting import plot_bar_chart, plot_time_series

def slugify(name: str) -> str:
    """
    Create a filesystem-safe slug from scenario name.
    Replace non-alphanumeric characters with underscore.
    """
    slug = re.sub(r'[^A-Za-z0-9._-]+', '_', name)
    return slug.strip('_')

def main():
    """
    Defines scenarios, runs simulations, and saves results to files.
    """
    # Load configuration
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    sim_params = config['simulation_parameters']
    scenarios = config['scenarios']
    output_files = config['output_files']
    
    # Create results directory
    output_dir = output_files['output_directory']
    os.makedirs(output_dir, exist_ok=True)
    
    # Set random seed for reproducible results
    random.seed(sim_params['random_seed'])
    np.random.seed(sim_params['random_seed'])
    
    # Dictionaries to store results
    summary_results = {}
    raw_results = {}
    
    print("Running simulations based on config.json...")
    
    # Run simulation for each scenario
    for name, params in scenarios.items():
        print(f"--- Running: {name} ---")
        summary, metrics = run_simulation(
            num_threads=params["num_threads"],
            arrival_rate=params["arrival_rate"],
            avg_service_time=params["avg_service_time"],
            sim_time=sim_params['simulation_time']
        )
        summary_results[name] = summary
        raw_results[name] = metrics
        print(f"Completed. Tasks completed: {summary['tasks_completed']}")

        # Save per-task CSV and queue CSV for this scenario
        slug = slugify(name)
        # Tasks CSV
        if metrics.task_records:
            tasks_df = pd.DataFrame.from_records(metrics.task_records)
            tasks_csv = os.path.join(output_dir, f"tasks_{slug}.csv")
            tasks_df.to_csv(tasks_csv, index=False)
            print(f"Saved per-task dataset to {tasks_csv}")
        else:
            print(f"No task records to save for scenario '{name}'.")

        # Queue CSV (timestamps + queue lengths)
        if metrics.queue_timestamps and metrics.queue_over_time:
            queue_df = pd.DataFrame({
                'time': metrics.queue_timestamps,
                'queue_length': metrics.queue_over_time
            })
            queue_csv = os.path.join(output_dir, f"queue_{slug}.csv")
            queue_df.to_csv(queue_csv, index=False)
            print(f"Saved queue time series dataset to {queue_csv}")
        else:
            print(f"No queue data to save for scenario '{name}'.")

    # Convert summary results to a DataFrame
    results_df = pd.DataFrame.from_dict(summary_results, orient='index')
    
    # Rename columns for clarity in the report
    results_df = results_df.rename(columns={
        'avg_wait': 'Average Wait Time',
        'avg_turnaround': 'Average Turnaround Time',
        'avg_queue': 'Average Queue Length',
        'utilization': 'Thread Pool Utilization (%)',
        'tasks_completed': 'Total Tasks Completed'
    })
    
    print("\n\n--- Simulation Results Summary ---")
    print(results_df.to_markdown(floatfmt=".2f"))
    
    # Save summary DataFrame to CSV
    csv_filename = os.path.join(output_dir, output_files['csv_summary'])
    results_df.to_csv(csv_filename)
    print(f"\nSummary results saved to {csv_filename}")
    
    # Generate and Save Visualizations
    print("Generating and saving plots...")
    
    # Generate Average Task Times Visualization
    plot_bar_chart(results_df[['Average Wait Time', 'Average Turnaround Time']],
                   'Average Task Times by Scenario', 
                   'Time Units',
                   os.path.join(output_dir, output_files['plot_task_times']))
    
    # Generate System State (Queue & Utilization) Visualization
    plot_bar_chart(results_df[['Average Queue Length', 'Thread Pool Utilization (%)']],
                   'Average Queue Length and Thread Utilization',
                   'Value',
                   os.path.join(output_dir, output_files['plot_system_state']))
    
    # Generate Queue Length Over Time Visualization
    plot_queue_key = output_files.get('plot_queue_over_time') or output_files.get('plot_queue_timeseries')
    plot_time_series(raw_results, 
                     'Queue Length Over Time', 
                     'Number of Tasks in Queue',
                     os.path.join(output_dir, plot_queue_key))
    
    print(f"\nAll plots and summary CSV have been saved to the '{output_dir}' folder.")

if __name__ == '__main__':
    main()
