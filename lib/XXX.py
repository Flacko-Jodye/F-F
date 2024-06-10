import json
from network import Network
from Arc import Arc
from Nodes import Node
from FF import FordFulkerson
import os
import time

# Load the JSON data
# data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'))

input_path = r'D:\Fub SS 2024\Metaheurisitk\F-F\Data\NEU_WORSTCASE_Instanz.json'
# input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_netgen_8_08a.json.json'

# ChatGPT Ergänzung
'''try:
    with open(input_path, 'r') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print(f"File not found: {input_path}")
    exit(1)'''
data= {'nodes': {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}, '6': {}, '7': {}, '8': {}, '9': {}, '10': {}, 'source': {}, 'sink': {}}, 'arcs': [{'start': '1', 'end': 'sink', 'capacity': 25}, {'start': 'source', 'end': '2', 'capacity': 3}, {'start': '3', 'end': 'sink', 'capacity': 7}, {'start': 'source', 'end': '4', 'capacity': 9}, {'start': 'source', 'end': '5', 'capacity': 10}, {'start': '6', 'end': 'sink', 'capacity': 5}, {'start': 'source', 'end': '7', 'capacity': 1}, {'start': '8', 'end': 'sink', 'capacity': 6}, {'start': 'source', 'end': '9', 'capacity': 10}, {'start': 'source', 'end': '10', 'capacity': 10}, {'start': '1', 'end': '2', 'capacity': 1.7320508075688772}, {'start': '1', 'end': '5', 'capacity': 2}, {'start': '2', 'end': '3', 'capacity': 10}, {'start': '2', 'end': '10', 'capacity': 8}, {'start': '3', 'end': '4', 'capacity': 1.5874010519681994}, {'start': '3', 'end': '7', 'capacity': 10}, {'start': '4', 'end': '5', 'capacity': 10}, {'start': '4', 'end': '6', 'capacity': 2}, {'start': '5', 'end': '6', 'capacity': 2}, {'start': '5', 'end': '7', 'capacity': 4}, {'start': '6', 'end': '7', 'capacity': 2}, {'start': '6', 'end': '10', 'capacity': 6}, {'start': '7', 'end': '8', 'capacity': 9}, {'start': '8', 'end': '9', 'capacity': 6}, {'start': '8', 'end': '10', 'capacity': 4}, {'start': '9', 'end': '10', 'capacity': 8}]}


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
    network.addArc(arc_data["start"], arc_data["end"], arc_data["capacity"])

# Timer starten
start_time = time.time()

# Max flow berechnen / # Iteration abspeichern für Visualisierung
output_dir = r"D:\Fub SS 2024\Metaheurisitk\F-F\Trash"
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

output_path = r"D:\Fub SS 2024\Metaheurisitk\F-F\Trash"
filename = "06.json"
with open(os.path.join(output_path, filename), "w") as outfile:
    json.dump(final_network, outfile)