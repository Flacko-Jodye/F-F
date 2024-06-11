import json
from network import Network
from Arc import Arc
from Nodes import Node
from FF_BFS import FordFulkerson
import os
import time
import math

# Load the JSON data
# data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'))

input_path = r'D:\Fub SS 2024\Metaheurisitk\F-F\Trash\irrelational_transform.json'
# input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_08a.json.json'

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


"Alte Version"
# # Knoten hinzufügen
# for node_data in data["nodes"]:
#     node = Node(node_data, node_data)
#     network.addNode(node)

# # Pfade dem Netzwerk hinzufügen
# for node_id in data["node"]:
#     source = (node_id == "source")
#     target = (node_id == "sink")
#     node = Node(id= node_id, source=source, target=target)
#     network.nodes[node_id] = node   

for arc_data in data["arcs"]:
    capacity = arc_data["capacity"]
    if isinstance(capacity, str):
        if "pi" in capacity or "e" in capacity:
            capacity = eval(capacity, {"pi": math.pi, "e": math.e})
        else:
            try:
                capacity = int(capacity)
            except ValueError:
                capacity = float(capacity)
    network.addArc(arc_data["start"], arc_data["end"], capacity)
# Timer starten
start_time = time.time()

# Max flow berechnen / # Iteration abspeichern für Visualisierung
output_dir = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/iterations"
max_flow = FordFulkerson(network, output_dir)

# Timer stoppen
end_time = time.time()

# Laufzeit berechnen
running_time = end_time - start_time

# Iteration abspeichern für Visualisierung

# Ergebnisse
print(f"Max flow: {max_flow}")
print(f"Laufzeit: {running_time} Sekunden")


# Graph abspeichern
# Kommentare löschen um neuen Graphen zu speichern
final_network = {
    "nodes": {node_id: {"source": node.source, "target": node.target} for node_id, node in network.nodes.items()},
    "arcs": [{"start": arc.start, "end": arc.end, "capacity": arc.capacity, "flow": arc.flow} for arc in network.getArcs()]
}
'''
utput_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/"
filename = "chvatal_small_final_network_graph.json"
with open(os.path.join(output_path, filename), "w") as outfile:
    json.dump(final_network, outfile)'''