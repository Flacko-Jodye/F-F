import json
import matplotlib.pyplot as plt
import os

def plot_core_usage(input_path, output_path):
    with open(input_path, "r") as infile:
        core_usages = json.load(infile)

    num_cores = len(core_usages[0])
    core_usage_over_time = {i: [] for i in range(num_cores)}

    for usage in core_usages:
        for i, core in enumerate(usage):
            core_usage_over_time[i].append(core)

    plt.figure(figsize=(15, 8))
    for core, usage in core_usage_over_time.items():
        plt.plot(usage, label=f'Core {core}')

    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.title('Core Usage Over Time')
    plt.legend()
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
