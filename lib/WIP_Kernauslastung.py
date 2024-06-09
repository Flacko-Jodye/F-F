import json
import matplotlib.pyplot as plt
import os

def plot_core_usage(input_path, output_path, max_points=500):
    with open(input_path, "r") as infile:
        core_usages = json.load(infile)
    
    # Extract core information
    physical_cores = core_usages.get('physical_cores', 'Unknown')
    logical_cores = core_usages.get('logical_cores', 'Unknown')
    
    # Normalize the timestamps to start from zero
    timestamps = core_usages['timestamps']
    core_usage_data = core_usages['core_usages']
    start_time = timestamps[0]
    normalized_timestamps = [t - start_time for t in timestamps]
    
    num_cores = len(core_usage_data[0])
    core_usage_over_time = {i: [] for i in range(num_cores)}

    for usage in core_usage_data:
        for i, core in enumerate(usage):
            core_usage_over_time[i].append(core)
    
    # Increase figure width
    plt.figure(figsize=(30, 8))

    # Limit the number of points to plot
    step = max(1, len(normalized_timestamps) // max_points)
    limited_timestamps = normalized_timestamps[::step]
    for core, usage in core_usage_over_time.items():
        plt.plot(limited_timestamps, usage[::step], label=f'Core {core}', alpha=0.75, linewidth=0.5)

    plt.xlabel('Zeit (Sekunden)')
    plt.ylabel('CPU Auslastung (%)')
    plt.title('CPU Auslastung über die Zeit')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1)
    # Add text about core information at the bottom of the plot
    plt.figtext(0.99, 0.01, f"Physical Cores: {physical_cores}, Logical Cores: {logical_cores}", horizontalalignment='right')
    
    # Set x-axis ticks to show only full values
    max_time = int(limited_timestamps[-1])
    plt.xticks(range(0, max_time + 1, max(1, max_time // 10)))  # Adjust tick interval based on total time

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    core_usage_files = [
        "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/Kernauslastung/Auslastung_Debug.json",
        "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/Kernauslastung/Auslastung_Flow.json",
        "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/Kernauslastung/Auslastung_Graph.json"
    ]
    for core_usage_file in core_usage_files:
        input_path = core_usage_file
        output_path = f"{os.path.splitext(core_usage_file)[0]}.png"
        plot_core_usage(input_path, output_path)
