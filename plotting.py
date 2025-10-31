import matplotlib.pyplot as plt

def plot_bar_chart(results_df, title, y_label, filename):
    """
    Helper function to create a bar chart from the results DataFrame
    and save it to a file.
    """
    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot on the created axis
    results_df.plot(kind='bar', ax=ax, rot=0)
    
    ax.set_title(title, fontsize=16)
    ax.set_ylabel(y_label, fontsize=12)
    ax.set_xlabel("Scenarios", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    fig.tight_layout()
    fig.savefig(filename) # Save the figure
    plt.close(fig) # Close the figure
    print(f"Plot saved to {filename}")

def plot_time_series(raw_results, title, y_label, filename):
    """
    Helper function to plot the queue length over time
    and save it to a file.
    """
    # Create a new figure
    fig, ax = plt.subplots(figsize=(12, 7)) 
    
    for scenario_name, metrics in raw_results.items():
        ax.plot(metrics.queue_timestamps, metrics.queue_over_time, 
                 label=scenario_name)
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Simulation Time", fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    ax.legend()
    ax.grid(linestyle='--', alpha=0.7)
    
    fig.tight_layout()
    fig.savefig(filename) # Save the figure
    plt.close(fig) # Close the figure
    print(f"Plot saved to {filename}")

