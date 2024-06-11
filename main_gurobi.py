import json
import networkx as nx
import matplotlib.pyplot as plt
from lib.lib_Gurobi import mf_solver
from networkx import bipartite_layout
import copy


# open JSON file
with open(r'C:\Users\fabia\OneDrive\Dokumente\Master_FU\Semester 2\Netzwerke\F&F\F-F\Data\transformed_netgen_8_13a.json','r') as f:
    data = json.load(f)

print(data.keys())

# extract nodes and arcs
nodes_dic = data['nodes']
arcs = data['arcs']

nodes=nodes_dic.keys()



# Problem solution
max_flow, flow_values = mf_solver.solve_mf(nodes, arcs, 'source', 'sink')

print(f"Max flow: {max_flow}")
print(f"Flow values:{flow_values}")



##### save flow values to a JSON file    
flow_values_str_keys = {str(key): value for key, value in flow_values.items()}

# Save flow_values to a JSON file
with open(r'C:\Users\fabia\OneDrive\Dokumente\Master_FU\Semester 2\Netzwerke\F&F\F-F\Data\chvatal_small_final_network_graph.json', 'w') as f:
    json.dump(flow_values_str_keys, f)

##################################################################################################
# Draw network

G = nx.DiGraph()

# add nodes
G.add_nodes_from(nodes)

# add arcs and capacity 
for arc in flow_values['arcs']:
    start = arc['start']
    end = arc['end']
    flow = arc['flow']
    capacity = arc['capacity']
    G.add_edge(start, end, flow=flow, capacity=capacity)

# Draw

pos = nx.spring_layout(G)  # positions for all nodes
labels = nx.get_edge_attributes(G, 'capacity')  # capacity of each arc
flow_labels = nx.get_edge_attributes(G, 'flow')  # flow of each arc

# combine capacity and flow values in one label

edge_labels = {(u, v): f"{flow}/ {capacity}" for (u, v), capacity, flow in zip(G.edges(), labels.values(), flow_labels.values())}



nx.draw_networkx_nodes(G, pos)  #draw nodes
nx.draw_networkx_edges(G, pos)  # draw arcs
nx.draw_networkx_labels(G, pos)  # draw labels for nodes
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # draw edge labels

# Add a text annotation at the bottom right
plt.text(1, 0, 'Flow/Capacity', horizontalalignment='right', verticalalignment='bottom', transform=plt.gca().transAxes)


plt.show()  # display
