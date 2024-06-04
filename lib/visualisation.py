import json
import networkx as nx
import matplotlib.pyplot as plt
import os

# NOch nicht fertig --> Graph ist sehr unübersichtlich
    # Welche Status sollte der Graph abbilden?
# Zu sehr großem Anteil von ChatGPT übernommen; einzelne Teile wurden selber angepasst, um Übersichtlichkeit zu gewährleisten

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
        if d['flow'] > 0:
            R.add_edge(v, u, capacity=0, flow=d['flow'])  # Add a residual edge from v to u with flow equal to the flow and capacity 0
        if d['capacity'] > d['flow']:
            R.add_edge(u, v, capacity=0, flow=d['capacity'] - d['flow'])  # Add a residual edge from u to v with flow equal to the remaining capacity and capacity 0

    # Positioning nodes: source on the left, sink on the right, others in the middle
    pos = nx.spring_layout(G, seed=42, k=1)

    # Fixing the positions of source and sink
    fixed_positions = {}
    for node_id in G.nodes():
        if data["nodes"][node_id]["source"]:
            fixed_positions[node_id] = (-1, 0)
        elif data["nodes"][node_id]["target"]:
            fixed_positions[node_id] = (1, 0)
    
    pos.update(fixed_positions)

    plt.figure(figsize=(16, 12))

    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="white", edgecolors="black")

    edge_labels = {}
    for u, v, d in G.edges(data=True):
        if d["flow"] > 0:
            label = f"{d['flow']}/{d['capacity']}"
            edge_labels[(u, v)] = label

    # Drawing regular edges with direction
    nx.draw_networkx_edges(G, pos, edgelist=edge_labels.keys(), arrowstyle='-|>', arrowsize=20, edge_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=10)

    # Draw residual edges with a slight curve and labels
    for u, v, d in R.edges(data=True):
        # Draw the residual edge if there is remaining capacity in the forward direction or there is flow in the backward direction
        if (G.has_edge(u, v) and G[u][v]['capacity'] > G[u][v]['flow']) or (G.has_edge(v, u) and G[v][u]['flow'] > 0):
            rad = 0.2  # increased curvature for better separation
            nx.draw_networkx_edges(R, pos, edgelist=[(u, v)], arrowstyle='-|>', style='dotted', edge_color='lightblue', arrowsize=20, alpha=0.5, connectionstyle=f'arc3,rad={rad}')
            # Adding edge labels for residual edges
            if G.has_edge(v, u) and G[v][u]['flow'] > 0:
                label = f"-{d['flow']}/0"  # Show the flow as negative and capacity as 0
            else:
                label = f"{d['flow']}/0"  # Show the flow as the remaining capacity and capacity as 0
            pos_mid = (pos[u] + pos[v]) / 2  # Position for the label
            plt.text(pos_mid[0], pos_mid[1] + 0.05, label, fontsize=10, color='lightblue', ha='center')  # Adjusted position

    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    visualize_final_graph()




"Copilot"

# import json
# import networkx as nx
# import matplotlib.pyplot as plt
# import os

# def visualize_final_graph(input_path="C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/chvatal_small_final_network_graph.json", output_path="Figures/final_graph_small.png"):
#     with open(input_path, "r") as infile:
#         data = json.load(infile)

#     G = nx.DiGraph()

#     for node_id in data["nodes"]:
#         G.add_node(node_id)

#     # Add edges with capacities and flows
#     for arc_data in data["arcs"]:
#         G.add_edge(arc_data["start"], arc_data["end"], capacity=arc_data["capacity"], flow=arc_data["flow"])

#     # Create a residual graph
#     R = nx.DiGraph()
#     for u, v, d in G.edges(data=True):
#         residual_capacity = d['capacity'] - d['flow']
#         if residual_capacity > 0:
#             R.add_edge(u, v, capacity=residual_capacity, flow=0)
#         if d['flow'] > 0:
#             R.add_edge(v, u, capacity=d['flow'], flow=0)

#     # Positioning nodes: source on the left, sink on the right, others in the middle
#     pos = nx.spring_layout(G, seed=42, k=1)  # Increased k for more spacing

#     # Fixing the positions of source and sink
#     fixed_positions = {}
#     for node_id in G.nodes():
#         if data["nodes"][node_id]["source"]:
#             fixed_positions[node_id] = (-1, 0)
#         elif data["nodes"][node_id]["target"]:
#             fixed_positions[node_id] = (1, 0)
    
#     pos.update(fixed_positions)  # update with fixed positions

#     # Create a figure with higher resolution
#     plt.figure(figsize=(16, 12))  # Higher resolution and larger figure size

#     # Draw nodes with circles around them
#     nx.draw_networkx_nodes(G, pos, node_size=700, node_color="white", edgecolors="black")

#     # Draw edges with labels for flow/capacity
#     edge_labels = {}
#     for u, v, d in G.edges(data=True):
#         if d["flow"] > 0:
#             label = f"{d['flow']}/{d['capacity']}"
#             edge_labels[(u, v)] = label

#     # Drawing regular edges with direction
#     nx.draw_networkx_edges(G, pos, edgelist=edge_labels.keys(), arrowstyle='-|>', arrowsize=20, edge_color='black')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=10)

#     # # Draw residual edges with a slight curve and labels
#     # for u, v, d in R.edges(data=True):
#     #     # Draw the residual edge if there is remaining capacity in the forward direction or there is flow in the backward direction
#     #     if (G.has_edge(u, v) and G[u][v]['capacity'] > G[u][v]['flow']) or (G.has_edge(v, u) and G[v][u]['flow'] > 0):
#     #         rad = 0.2  # increased curvature for better separation
#     #         nx.draw_networkx_edges(R, pos, edgelist=[(u, v)], arrowstyle='-|>', style='dotted', edge_color='lightblue', arrowsize=20, alpha=0.5, connectionstyle=f'arc3,rad={rad}')
#     #         # Adding edge labels for residual edges
#     #         label = f"{d['capacity']}/{d['capacity']}"  # Residual edges have their own capacities
#     #         pos_mid = (pos[u] + pos[v]) / 2  # Position for the label
#     #         plt.text(pos_mid[0], pos_mid[1] + 0.05, label, fontsize=10, color='lightblue', ha='center')  # Adjusted position

#     # Draw residual edges with a slight curve and labels
#     for u, v, d in R.edges(data=True):
#         # Draw the residual edge if there is remaining capacity in the forward direction or there is flow in the backward direction
#         if (G.has_edge(u, v) and G[u][v]['capacity'] > G[u][v]['flow']) or (G.has_edge(v, u) and G[v][u]['flow'] > 0):
#             rad = 0.2  # increased curvature for better separation
#             nx.draw_networkx_edges(R, pos, edgelist=[(u, v)], arrowstyle='-|>', style='dotted', edge_color='lightblue', arrowsize=20, alpha=0.5, connectionstyle=f'arc3,rad={rad}')
#             # Adding edge labels for residual edges
#             if G.has_edge(v, u) and G[v][u]['flow'] > 0:
#                 label = f"-{G[v][u]['flow']}/0"  # Show the flow as negative and capacity as 0
#             else:
#                 label = f"0/{d['capacity']}"  # Show the flow as 0 and capacity as the remaining capacity
#             pos_mid = (pos[u] + pos[v]) / 2  # Position for the label
#             plt.text(pos_mid[0], pos_mid[1] + 0.05, label, fontsize=10, color='lightblue', ha='center')  # Adjusted position

#     # Draw node labels
#     nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

#     # Ensure the Figures directory exists
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     # Save the figure with higher resolution
#     plt.savefig(output_path, dpi=300)  # Save at 300 dpi
#     plt.close()

# # For standalone run
# if __name__ == "__main__":
#     visualize_final_graph()
