import ast
import time
import os
import psutil
from libr import mcf_solver
import json
import networkx as nx
import matplotlib.pyplot as plt

from networkx import bipartite_layout
import copy


# open JSON file
with open(r'D:\Fub SS 2024\Metaheurisitk\F-F\Data\netgen_8_13a.json','r') as f:
    data = json.load(f)

print(data.keys())


# extract nodes and arcs
nodes= data['nodes']
arcs = data['arcs']



# CPU / Memory Tracking
process = psutil.Process(os.getpid())
cpu_start = process.cpu_percent(interval = None)
memory_info_start = process.memory_info()

# Kernauslastung tracken
core_usages = []
timestamps = []

# Kerne tracken
def log_core_usage():
    core_usages.append(psutil.cpu_percent(interval=None, percpu=True))
    timestamps.append(time.time())



# Problem solution
min_cost, flow_values = mcf_solver.solve_mcf(nodes, arcs)



# CPU / Memory stoppen
cpu_end = process.cpu_percent(interval= None)
memory_info_end = process.memory_info()

cpu_auslastung = (cpu_end - cpu_start) / psutil.cpu_count()
memory_usage = process.memory_info().rss

physical_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)




print(f"Min_cost: {min_cost}")
print(f"Flow values:{flow_values}")

print(f"Number of physical cores: {physical_cores}")
print(f"Number of logical cores: {logical_cores}")

print(f"CPU Auslastung: {cpu_auslastung}%")
print(f"Speicherverbrauch: {memory_usage / (1024*1024):.2f} MB")


core_usage_data = {
    "timestamps": timestamps,
    "core_usages": core_usages,
    "physical_cores": physical_cores,
    "logical_cores": logical_cores
}



##### save flow values to a JSON file    
flow_values_str_keys = {str(key): value for key, value in flow_values.items()}

# Save flow_values to a JSON file
with open(r'D:\Fub SS 2024\Metaheurisitk\F-F\Data\08_13a.json', 'w') as f:
    json.dump(flow_values_str_keys, f)

# Kernauslastung abspeichern
core_usage_path = r"D:\Fub SS 2024\Metaheurisitk\F-F\Gurobi_Min_Cost\Output\Output_ohne_Startl\Kernelauslastung_08_13a.json"
with open(core_usage_path, "w") as outfile:
    json.dump(core_usage_data, outfile)
print(f"Kernauslastung abgespeichert unter {core_usage_path}")

##################################################################################################
# Draw network

G = nx.DiGraph()

# add nodes
G.add_nodes_from(nodes)

# add arcs and capacity 
for arc in arcs:
    G.add_edge(arc['from'], arc['to'], capacity=arc['upper_bound'])

# flow values
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
edge_labels = {(u, v): f"{flow_labels[(u, v)]}/{labels[(u, v)]}" for (u, v) in G.edges()}


nx.draw_networkx_nodes(G, pos)  #draw nodes
nx.draw_networkx_edges(G, pos)  # draw arcs
nx.draw_networkx_labels(G, pos)  # draw labels for nodes
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # draw edge labels

# Add a text annotation at the bottom right
plt.text(1, 0, 'Flow/Capacity', horizontalalignment='right', verticalalignment='bottom', transform=plt.gca().transAxes)


plt.show()  # display


