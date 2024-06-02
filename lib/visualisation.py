import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def visualize_final_graph(input_path="C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/chvatal_small_final_network_graph.json", output_path="Figures/final_graph_small.png"):
    with open(input_path, "r") as infile:
        data = json.load(infile)

    G = nx.DiGraph()

    for node_id in data["nodes"]:
        G.add_node(node_id)

    # Add edges with capacities and flows
    for arc_data in data["arcs"]:
        G.add_edge(arc_data["start"], arc_data["end"], capacity=arc_data["capacity"], flow=arc_data["flow"])

    # Create a residual graph
    R = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        # Forward edge in the residual graph
        if d['capacity'] > 0:
            residual_capacity = d['capacity'] - d['flow']
            if residual_capacity > 0:
                R.add_edge(u, v, capacity=residual_capacity, flow=0)
        # Reverse edge in the residual graph
        if d['flow'] > 0:
            R.add_edge(v, u, capacity=d['flow'], flow=0)

    # Positioning nodes: source on the left, sink on the right, others in the middle
    pos = nx.spring_layout(G, seed=42, k=1)  # Increased k for more spacing

    # Fixing the positions of source and sink
    fixed_positions = {}
    for node_id in G.nodes():
        if data["nodes"][node_id]["source"]:
            fixed_positions[node_id] = (-1, 0)
        elif data["nodes"][node_id]["target"]:
            fixed_positions[node_id] = (1, 0)
    
    pos.update(fixed_positions)  # update with fixed positions

    # Create a figure with higher resolution
    plt.figure(figsize=(16, 12))  # Higher resolution and larger figure size

    # Draw nodes with circles around them
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="white", edgecolors="black")

    # Draw edges with labels for flow/capacity
    edge_labels = {}
    for u, v, d in G.edges(data=True):
        label = f"{d['flow']}/{d['capacity']}"
        edge_labels[(u, v)] = label

    # Drawing regular edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrowstyle='->', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=10)

    # Draw residual edges with a slight curve and labels
    for u, v, d in R.edges(data=True):
        rad = 0.2  # increased curvature for better separation
        nx.draw_networkx_edges(R, pos, edgelist=[(u, v)], arrowstyle='->', style='dotted', edge_color='#3399FF', arrowsize=20, alpha=0.5, connectionstyle=f'arc3,rad={rad}')
        # Adding edge labels for residual edges
        label = f"{d['capacity']}/{d['capacity']}"  # Residual edges have their own capacities
        pos_mid = (pos[u] + pos[v]) / 2  # Position for the label
        plt.text(pos_mid[0], pos_mid[1] + 0.05, label, fontsize=12, color='blue', ha='center')  # Adjusted position

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    # Ensure the Figures directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the figure with higher resolution
    plt.savefig(output_path, dpi=300)  # Save at 300 dpi
    plt.close()

# For standalone run
if __name__ == "__main__":
    visualize_final_graph()
