import json
import os

import psutil
from lib.Nodes import Node
import time
from lib.settings import Settings
from lib.networkInput import NetworkInput
from lib.network import Network
from lib import helper
from lib. transformation import transform_data

Suchmethode = "DFS" # Hier geben wir an, ob wir DFS oder BFS verwenden wollen,damit der richtige Algorithmus aufgerufen wird
if Suchmethode == "DFS":
    from lib.WIP_FF import FordFulkerson_Graph
elif Suchmethode == "BFS":
    from lib.FF_BFS import FordFulkerson_Graph
    
input_filename = "chvatal_small.json"

data_original=json.load(open(f"Data/{input_filename}"))

print("Data wird transformiert")
if "sink" not in data_original["nodes"]:
    transform_data(f"Data/{input_filename}",f"Data/transformed_{input_filename}")
    data_transformed =json.load(open(f"Data/transformed_{input_filename}"))
    data=data_transformed
else:
    print("Data ist bereits für das FF-Problem")
    data = data_original	
print("Data wurde transformiert")

inputpfad_transformation=  f"Data/transformed_{input_filename}"

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
output_dir = "Data/iterations"
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

output_path = f"Data/{input_filename}"

with open(output_path, "w") as outfile:
    json.dump(final_network, outfile)
print(f"Max Flow Graph abgespeichert unter {output_path}")
# Kernauslastung abspeichern
core_usage_path = f"Output/FF_Output/Auslastung_Flow{input_filename}"
with open(core_usage_path, "w") as outfile:
    json.dump(core_usage_data, outfile)
print(f"Kernauslastung abgespeichert unter {core_usage_path}")


