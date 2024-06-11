# Einzelne Schritte in Folge vom Graph Modus visualisieren
import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def visualize_step(input_path, output_path, pos):
    with open(input_path, "r") as infile:
        data = json.load(infile)

    G = nx.DiGraph()

    for node_id in data["nodes"]:
        G.add_node(node_id)

    for arc_data in data["arcs"]:
        G.add_edge(arc_data["start"], arc_data["end"], capacity=arc_data["capacity"], flow=arc_data["flow"])

# Augmenting paths extra getten sowie die Anfangskanten
    augmenting_path = set(tuple(arc) for arc in data.get("augmenting_path", []))  

    
    plt.figure(figsize=(20, 12))

    source_node = "source"
    sink_node = "sink"
    normale_nodes = [node for node in G.nodes if node not in [source_node, sink_node]]
    nx.draw_networkx_nodes(G, pos, nodelist=normale_nodes, node_size=700, node_color="white", edgecolors="black")
    nx.draw_networkx_nodes(G, pos, nodelist=[source_node], node_size=700, node_color="green", edgecolors="black")
    nx.draw_networkx_nodes(G, pos, nodelist=[sink_node], node_size=700, node_color="red", edgecolors="black")

    edge_labels = {}
    edge_colors = []

    for u, v, d in G.edges(data=True):
        label = f"{d['flow']}/{d['capacity']}"
        edge_labels[(u, v)] = label

        color = "orange" if (u, v) in augmenting_path else "black"  
        edge_colors.append(color)
    nx.draw_networkx_edges(G, pos, edgelist=edge_labels.keys(), arrowstyle="-|>", arrowsize=20, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=10)

    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    plt.text(1, 0, 'Flow/Capacity', horizontalalignment='right', verticalalignment='bottom', transform=plt.gca().transAxes)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved visualization to {output_path}")  # Debugging statement

if __name__ == "__main__":
    iteration_dir = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/iterations"
    output_dir = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Figures/Iterationen"
    print(f"Reading from {iteration_dir}...")  # New: added print statements for debugging
    print(f"Saving to {output_dir}...")  # New: added print statements for debugging
    iteration_files = sorted(os.listdir(iteration_dir))

# Statische Positionen für die Knoten
    with open(os.path.join(iteration_dir, iteration_files[0]), "r") as infile:
        data = json.load(infile)
    G = nx.DiGraph()
    for node_id in data["nodes"]:
        G.add_node(node_id)
    for arc_data in data["arcs"]:
        G.add_edge(arc_data["start"], arc_data["end"], capacity=arc_data["capacity"], flow=arc_data["flow"])
    pos = nx.kamada_kawai_layout(G)  # Static positions

    # Manuelle Knotenpositionen
    pos = {
        'source': [-1, 0],
        'sink': [1, 0],
        '1': [0.4, 0.5],
        '2': [0.255, -0.25],
        '3': [0, 1],
        '4': [0, -1],
        '5': [-0.5, 0.5],
        '6': [-0.5, -0.5]
    }




    for iteration_file in iteration_files:
        if iteration_file.endswith(".json"):
            input_path = os.path.join(iteration_dir, iteration_file)
            output_path = os.path.join(output_dir, f"{os.path.splitext(iteration_file)[0]}.png")
            print(f"Processing {iteration_file}...")  # Debugging statement
            visualize_step(input_path, output_path, pos)

    print("All visualizations created.") # Debugging statement


