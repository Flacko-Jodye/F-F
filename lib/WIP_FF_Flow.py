# Gibt den Max-Flow wieder ohne dass Zwischnschritte geprintet werden oder JSONs zur Visualisierung erstellt werden.
# Ziel

import json
from lib.network import Network
from lib.Arc import Arc
from lib.Nodes import Node
# from WIP_FF import FordFulkerson_Flow
from lib.WIP_BFS import FordFulkerson_Flow
import os
import time
import psutil

# Load the JSON data
# data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'))

input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'
# input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_08a.json.json'
# input_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_13a.json"

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

# Max flow berechnen
max_flow, iterations, s_cut, t_cut = FordFulkerson_Flow(network, log_core_usage)

# Timer stoppen / Laufzeit
end_time = time.time()

# CPU / Memory stoppen
cpu_end = process.cpu_percent(interval= None)
memory_info_end = process.memory_info()

# Laufzeiten berechnen
running_time = end_time - start_time
cpu_auslastung = (cpu_end - cpu_start) / psutil.cpu_count()
memory_usage = process.memory_info().rss
# memory_usage = memory_info_start.rss - memory_info_end.rss


process = process.memory_info().rss # "????"

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

# Kernauslastung abspeichern
core_usage_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/Kernauslastung/Auslastung_Flow.json"
with open(core_usage_path, "w") as outfile:
    json.dump(core_usage_data, outfile)
print(f"Kernauslastung abgespeichert unter {core_usage_path}")