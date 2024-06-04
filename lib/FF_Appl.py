import json
from network import Network
from Arc import Arc
from Nodes import Node
from FF import FordFulkerson
import os
import time

# Load the JSON data
# data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'))

input_path = 'C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'

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
    network.addArc(arc_data["start"], arc_data["end"], arc_data["capacity"])

# Timer starten
start_time = time.time()

# Calculate max flow
max_flow = FordFulkerson(network)

# Timer stoppen
end_time = time.time()

# Laufzeit berechnen
running_time = end_time - start_time

# Ergebnisse
print(f"Max flow: {max_flow}")
print(f"Laufzeit: {running_time} Sekunden")


# Graph abspeichern
# Kommentare löschen um neuen Graphen zu speichern
final_network = {
    "nodes": {node_id: {"source": node.source, "target": node.target} for node_id, node in network.nodes.items()},
    "arcs": [{"start": arc.start, "end": arc.end, "Kapazität": arc.capacity, "flow": arc.flow} for arc in network.getArcs()]
}

output_path = "C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/"
filename = "chvatal_small_final_network_graph.json"
with open(os.path.join(output_path, filename), "w") as outfile:
    json.dump(final_network, outfile)