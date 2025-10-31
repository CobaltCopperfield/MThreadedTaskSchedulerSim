# Multi-Threaded Task Scheduler Simulation
This project uses SimPy (a Python library) to simulate and test a multi-threaded task scheduler.

You can run different tests to see how things like wait times or queue lengths change when you adjust the number of threads or how many tasks arrive.

## Project Structure
The project is split into these files:
* `main.py`: This is the main script you run. It reads the config, runs the tests, and saves the results.
* `config.json`: All settings are in this file. Edit this file to change tests or settings.
* `simulation_model.py`: Has the core simulation logic (like how tasks are created and run).
* `plotting.py`: Creates the charts and graphs for the results.
* `results/`: A folder that is automatically created to hold all output (CSV files and plots).

## Dependencies
You will need these Python libraries:
* `simpy`: The core simulation engine.
* `pandas`: Used for organizing and exporting results.
* `numpy`: Used for statistical calculations (mean) and managing random seeds.
* `matplotlib`: Used for generating plots.

## Installation
1. Ensure you have Python 3.6 or newer installed.
2. Install the required libraries using pip:
`pip install -r <path for requirements.txt>`

## How to Run
1. Navigate to the project directory.
2. Run the main script from your appropriate terminal:
`python main.py`
3. The script will print status updates to the console, including a final Markdown table of the results.
4. All output files will be saved in the `results/` folder.

## How to Configure Experiments
To change simulation parameters or add new scenarios, edit the `config.json` file.

### Changing Parameters
You can change the total simulation time or the random seed under `simulation_parameters`. You can also change the names of output files under `output_files`.
```
{
  "simulation_parameters": {
    "simulation_time": 2000,
    "random_seed": 6
  },
  "output_files": {
    "output_directory": "results",
    "csv_summary": "simulation_results_summary.csv",
    ...
  },
  ...
}
```

### Adding a New Scenario
To add a new experiment, simply add a new object to the `scenarios` dictionary in `config.json`. The key will be used as the label in the final report and plots.

### Example: Adding a "High Capacity" scenario
```
{
  ...
  "scenarios": {
    ...,
    "4. High Capacity (10T, 1.0 Load)": {
      "num_threads": 10,
      "arrival_rate": 1.0,
      "avg_service_time": 5.0
    }
  }
}
```
When you run `python main.py` again, this new scenario will be automatically included in the simulation, the results table, and all generated plots.

## Output
After running, you will find the following files in the `results/` directory:
* `simulation_results_summary.csv`: A CSV file containing the summary table of key metrics for all scenarios.
* `task_times_summary.png`: A bar chart comparing average wait and turnaround times.
* `system_state_summary.png`: A bar chart comparing average queue length and thread utilization.
* `queue_length_over_time.png`: A line plot showing the queue length over the duration of the simulation for each scenario.
