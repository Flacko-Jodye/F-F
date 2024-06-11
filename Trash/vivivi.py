import json
import networkx as nx
import matplotlib.pyplot as plt
import os

# NOch nicht fertig --> Graph ist sehr unübersichtlich
    # Welche Status sollte der Graph abbilden?
# Zu sehr großem Anteil von ChatGPT übernommen; einzelne Teile wurden selber angepasst, um Übersichtlichkeit zu gewährleisten

def visualize_final_graph(input_path=r"D:\Fub SS 2024\Metaheurisitk\F-F\Data\BFSchvatal_small_final_network_graph.json"):
    with open(input_path, "r") as infile:
        data = json.load(infile)
# def visualize_final_graph(input_path="C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_08a.json", output_path="Figures/final_graph_Big.png"):
#     with open(input_path, "r") as infile:
#         data = json.load(infile)

    G = nx.DiGraph()

    for node_id in data["nodes"]:
        G.add_node(node_id)

    # Add edges with capacities and flows
    for arc_data in data["arcs"]:
        G.add_edge(arc_data["start"], arc_data["end"], capacity=arc_data["capacity"], flow=arc_data["flow"])

   

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
    nx.draw_networkx_labels(G, pos) 
    
    
    plt.show()


    #######################################################
     # Create a residual graph
    R = nx.DiGraph()

    for node_id in data["nodes"]:
        R.add_node(node_id)

    for u, v, d in G.edges(data=True):
        if d['flow'] > 0:
            R.add_edge(v, u, capacity=0, flow=-d['flow'])  # Add a residual edge from v to u with flow equal to the flow and capacity 0
        if d['capacity'] > d['flow']:
            R.add_edge(u, v, capacity=d['capacity'] ,flow=d['flow'])  # Add a residual edge from u to v with flow equal to the remaining capacity and capacity 0

    #Position of nodes and edges

    #Nodes
    pos = nx.spring_layout(R, seed=42, k=1)  # Positioning nodes: source on the left, sink on the right, others in the middle

        # Fixing the positions of source and sink
    fixed_positions = {}   
    for node_id in G.nodes():
        if data["nodes"][node_id]["source"]:
            fixed_positions[node_id] = (-1, 0)
        elif data["nodes"][node_id]["target"]:
            fixed_positions[node_id] = (1, 0)
    
    pos.update(fixed_positions)

    plt.figure(figsize=(16, 12))

        # Draw nodes with circles around them
    nx.draw_networkx_nodes(R, pos, node_size=700, node_color="white", edgecolors="black")
        # Draw nodenames
    nx.draw_networkx_labels(R, pos) 


    #edges：
    
        # Forward edges  with solid black lines
            
    forward_edges = [(u, v)  for u, v, d in R.edges(data=True) if d.get('capacity', 0) > 0]
    nx.draw_networkx_edges(R, pos, edgelist=forward_edges, edge_color='black', arrowstyle='-|>', arrowsize=20)
           
        # backward edges with dotted light blue lines
    backward_edges = [(u, v)  for u, v, d in R.edges(data=True) if d.get('capacity', 0) == 0]
    rad = 0.2  # increased curvature for better separation
    nx.draw_networkx_edges(R, pos, edgelist=backward_edges, arrowstyle='-|>', style='dotted', edge_color='lightblue', arrowsize=20, alpha=0.5, connectionstyle=f'arc3,rad={rad}')       
    
        # forward edge labels (showing remaining capacity)
    forward_edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in R.edges(data=True) if d.get('capacity', 0) > 0}
    nx.draw_networkx_edge_labels(R, pos, edge_labels=forward_edge_labels, font_color='black', font_size=10)
        # backward edge labels (showing flow)
    backward_edge_labels = {(u, v): f"{d['flow']}/{d['capacity']}" for u, v, d in R.edges(data=True) if d.get('capacity', 0) == 0}
    for (u, v), flow in backward_edge_labels.items():
        label = str(flow)
        pos_mid = ((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2 + 0.1)  # Adjusted position for the label
        plt.text(pos_mid[0], pos_mid[1], label, fontsize=10, color='lightblue', ha='center')  # Draw the label


    plt.show()

    
if __name__ == "__main__":
    visualize_final_graph()

