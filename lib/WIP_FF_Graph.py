# Große Teile des Codes für die Metriken (z.B. CPU-Auslastung) wurden von Copilot übernommen.
import json
from lib.network import Network
from lib.Arc import Arc
from lib.Nodes import Node
# Wählen ob normaler FF-Algorithmus mit DFS oder mit BFS (Edmonds-Karp)
from WIP_FF import FordFulkerson_Graph
# from WIP_BFS import FordFulkerson_Graph

import os
import time
import psutil


input_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'transformed_start_end.json')

# Load the JSON data
# input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'
# input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_08a.json.json'
# input_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/NEU_WORSTCASE_Instanz_Anderer_Weg.json"

# ChatGPT Ergänzung
try:
    with open(input_path, 'r') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print(f"File not found: {input_path}")
    exit(1)

# Netzwerk erstellen
network = Network()

# CHatGPT Alternative
for node_id in data["nodes"]:
    source = (node_id == "source")
    target = (node_id == "sink")
    node = Node(id = node_id, source = source, target = target)
    print(f"Initialized node {node.id}: source={node.source}, target={node.target}")
    network.nodes[node_id] = node

for arc_data in data["arcs"]:
    network.addArc(arc_data["start"], arc_data["end"], arc_data["capacity"])

# Timer starten
start_time = time.time()

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

# Max flow berechnen / # Iteration abspeichern für Visualisierung
output_dir = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/iterations"
# max_flow = FordFulkerson_Graph(network, output_dir, log_core_usage)


max_flow, iterations, s_cut, t_cut = FordFulkerson_Graph(network, output_dir, log_core_usage)
# Timer stoppen
end_time = time.time()

# CPU / Memory stoppen
cpu_end = process.cpu_percent(interval= None)
memory_info_end = process.memory_info()

# Laufzeiten berechnen
running_time = end_time - start_time
cpu_auslastung = (cpu_end - cpu_start) / psutil.cpu_count()
memory_usage = process.memory_info().rss

# Laufzeit berechnen
running_time = end_time - start_time

# Iteration abspeichern für Visualisierung

# Ergebnisse
print(f"Max flow: {max_flow}")
print(f"Laufzeit: {running_time} Sekunden")

print(f"Number of iterations: {iterations}")
print(f"s-t cut: s-cut = {s_cut}, t-cut = {t_cut}")

physical_cores = psutil.cpu_count(logical=False)
logical_cores = psutil.cpu_count(logical=True)

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

# Graph abspeichern
# Kommentare löschen um neuen Graphen zu speichern
final_network = {
    "nodes": {node_id: {"source": node.source, "target": node.target} for node_id, node in network.nodes.items()},
    "arcs": [{"start": arc.start, "end": arc.end, "capacity": arc.capacity, "flow": arc.flow} for arc in network.getArcs()]
}

output_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/"
filename = "chvatal_small_final_network_graph.json"
with open(os.path.join(output_path, filename), "w") as outfile:
    json.dump(final_network, outfile)

# Kernauslastung abspeichern
core_usage_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/Kernauslastung/Auslastung_Graph.json"
with open(core_usage_path, "w") as outfile:
    json.dump(core_usage_data, outfile)
print(f"Kernauslastung abgespeichert unter {core_usage_path}")























"Alte Version"

# import json
# from network import Network
# from Arc import Arc
# from Nodes import Node
# from FF import FordFulkerson
# import os
# import time

# # Load the JSON data
# # data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'))

# input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'
# # input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_08a.json.json'

# # ChatGPT Ergänzung
# try:
#     with open(input_path, 'r') as infile:
#         data = json.load(infile)
# except FileNotFoundError:
#     print(f"File not found: {input_path}")
#     exit(1)

# # Netzwerk erstellen
# network = Network()

# # CHatGPT Alternative
# for node_id in data["nodes"]:
#     source = (node_id == "source")
#     target = (node_id == "sink")
#     node = Node(id = node_id, source = source, target = target)
#     print(f"Initialized node {node.id}: source={node.source}, target={node.target}")
#     network.nodes[node_id] = node


# "Alte Version"
# # # Knoten hinzufügen
# # for node_data in data["nodes"]:
# #     node = Node(node_data, node_data)
# #     network.addNode(node)

# # # Pfade dem Netzwerk hinzufügen
# # for node_id in data["node"]:
# #     source = (node_id == "source")
# #     target = (node_id == "sink")
# #     node = Node(id= node_id, source=source, target=target)
# #     network.nodes[node_id] = node   

# for arc_data in data["arcs"]:
#     network.addArc(arc_data["start"], arc_data["end"], arc_data["capacity"])

# # Timer starten
# start_time = time.time()

# # Max flow berechnen / # Iteration abspeichern für Visualisierung
# output_dir = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/iterations"
# max_flow = FordFulkerson(network)

# # Timer stoppen
# end_time = time.time()

# # Laufzeit berechnen
# running_time = end_time - start_time

# # Iteration abspeichern für Visualisierung

# # Ergebnisse
# print(f"Max flow: {max_flow}")
# print(f"Laufzeit: {running_time} Sekunden")


# # Graph abspeichern
# # Kommentare löschen um neuen Graphen zu speichern
# final_network = {
#     "nodes": {node_id: {"source": node.source, "target": node.target} for node_id, node in network.nodes.items()},
#     "arcs": [{"start": arc.start, "end": arc.end, "capacity": arc.capacity, "flow": arc.flow} for arc in network.getArcs()]
# }

# output_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/"
# filename = "chvatal_small_final_network_graph.json"
# with open(os.path.join(output_path, filename), "w") as outfile:
#     json.dump(final_network, outfile)