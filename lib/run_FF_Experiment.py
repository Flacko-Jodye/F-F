from network import Network
from Arc import Arc
from Nodes import Node
from WIP_FF_Debug import FordFulkerson_Debug  # Assuming your main functions are in WIP_FF_Debug.py
import json
import random
import matplotlib.pyplot as plt

# Function to log core usage (placeholder)
def log_core_usage():
    pass

def create_network_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    network = Network()

    # Add nodes
    for node_id in data["nodes"]:
        is_source = node_id == "source"
        is_sink = node_id == "sink"
        node = Node(node_id, is_source, is_sink)
        network.addNode(node)

    # Add arcs
    for arc in data["arcs"]:
        start, end, capacity = arc["start"], arc["end"], arc["capacity"]
        arc_obj = Arc(start, end, capacity)
        network.addArc(arc_obj)

    return network

def run_experiment(runs=100):
    iterations_list = []

    for _ in range(runs):
        network = create_network_from_json('"C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/Worst_Case_Random.json"')
        _, iterations, _, _ = FordFulkerson_Debug(network, log_core_usage)
        iterations_list.append(iterations)

    return iterations_list

def plot_iterations(iterations_list):
    plt.hist(iterations_list, bins=range(min(iterations_list), max(iterations_list) + 1), edgecolor='black')
    plt.title('Distribution of Ford-Fulkerson Algorithm Iterations')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    iterations_list = run_experiment(100)
    print(f"Iterations for each run: {iterations_list}")
    plot_iterations(iterations_list)
