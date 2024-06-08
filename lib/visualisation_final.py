import json
import networkx as nx
import matplotlib.pyplot as plt
import os

# To-Do:
    # Reihenfolge anpassen
    # Labels anpassen

def visualise_final_graph(input_path="C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/chvatal_small_final_network_graph.json", output_path="Figures/final_graph_small.png"):
    with open(input_path, "r") as infile:
        data = json.load(infile)

    G = nx.DiGraph()

    for node_id in data["nodes"]:
        G.add_node(node_id)

    # Add edges with capacities and flows
    for arc_data in data["arcs"]:
        G.add_edge(arc_data["start"], arc_data["end"], capacity=arc_data["capacity"], flow=arc_data["flow"])

    # Positioning nodes: source on the left, sink on the right, others in the middle
    pos = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(20, 14))

    # Knoten
    source_node = "source"
    sink_node = "sink"

    # Knoten zeichnen
    normale_nodes = [node for node in G.nodes if node not in [source_node, sink_node]]
    nx.draw_networkx_nodes(G, pos, nodelist=normale_nodes, node_size=700, node_color="white", edgecolors="black")
    # nx.draw_networkx_nodes(G, pos, nodelist=[source_node], node_size=700, node_color="lightgreen", edgecolors="black")
    nx.draw_networkx_nodes(G, pos, nodelist=[source_node], node_size=700, node_color="white", edgecolors="black")
    nx.draw_networkx_nodes(G, pos, nodelist=[sink_node], node_size=700, node_color="#f1807e", edgecolors="black")
    
    # nx.draw_networkx_nodes(G, pos, node_size=700, node_color="white", edgecolors="black")

    # Create a residual graph
    R = nx.DiGraph()
    for u, v, d in G.edges(data=True):
        residual_capacity = d['capacity'] - d['flow']

        # Auskommentiert, um nicht negative Residualkanten auszuschließen
        # if residual_capacity > 0:
        #     R.add_edge(u, v, capacity=residual_capacity, flow=0)
        if d['flow'] > 0:
            R.add_edge(v, u, capacity=d['flow'], flow=0)

    edge_labels = {}
    for u, v, d in G.edges(data=True):
        if d["flow"] > 0 or d["capacity"] > 0:
            label = f"{d['flow']}/{d['capacity']}"
            edge_labels[(u,v)] = label
    radG = 0
    # Drawing regular edges with direction
    nx.draw_networkx_edges(G, pos, edgelist=edge_labels.keys(), arrowstyle="-|>", arrowsize=20, edge_color="black", connectionstyle=f"arc3,rad={radG}")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=10)

    # Draw residual edges with a slight curve and labels
    residual_edge_labels = {}
    for u, v, d in R.edges(data=True):
        if (G.has_edge(u, v) and G[u][v]['capacity'] > G[u][v]['flow'] and d["flow"] == 0 ) or (G.has_edge(v, u) and G[v][u]['flow'] > 0 and d["flow"] == 0): #or (G.has_edge(v, u) and G[v][u]['flow'] > 0 and G[u][v]["flow"] > 0 and G[v][u]["flow"] ):
            rad = 0.3  # increased curvature for better separation
            nx.draw_networkx_edges(R, pos, edgelist=[(u, v)], arrowstyle='-|>', style='dotted', edge_color='blue', arrowsize=20, alpha=0.5, connectionstyle=f'arc3,rad={rad}')
            # Adding edge labels for residual edges
            if G.has_edge(v, u) and G[v][u]['flow'] > 0:
                label = f"-{d['capacity']}/{d['flow']}"  # Show the flow as negative and capacity as 0
            else:
                label = f"{d['capacity']}/{d['flow']}"  # Show the flow as the remaining capacity and capacity as 0
            residual_edge_labels[(u, v)] = label
            # plt.text(pos_mid[0], pos_mid[1] + 0.05, label, fontsize=10, color='blue', ha='center')  # Adjusted position
    
    "Copilot"
    # Positionen der Labels
    for (u, v), label in residual_edge_labels.items():
        x = pos[u][0] * 0.5 + pos[v][0] * 0.5
        y = pos[u][1] * 0.5 + pos[v][1] * 0.5
        offset = 0.05
        if pos[v][1] > pos[u][1]:  # If the end node is above the start node
            x += offset
            y += offset  # Move the label up
        else:  # If the end node is below the start node
            y -= offset  # Move the label down
            y -= offset 
        plt.text(x, y, label, color='blue', fontsize=10, ha='center', va='center', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.2'))
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")


    plt.text(1, 0, 'Flow/Capacity', horizontalalignment='right', verticalalignment='bottom', transform=plt.gca().transAxes)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    visualise_final_graph()