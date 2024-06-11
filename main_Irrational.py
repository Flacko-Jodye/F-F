import json
import os

from lib.transformation import transform_data
import json
from lib.network import Network
from lib.Arc import Arc
from lib.Nodes import Node
from lib.FF_irrational_Kapazität import FordFulkerson
import os
import time
import math

input_filename = "Irrational_Kapa.json"

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


######### FF-Ausführung #########

print("Max-Flow-Problem wird gelöst")
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
    capacity = arc_data["capacity"]
    if isinstance(capacity, str): # weil in Datensaetzen pi und e vorkommen könnten
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
output_dir = "Data/iterations"
max_flow = FordFulkerson(network, output_dir)


# Timer stoppen
end_time = time.time()

print(f"Iterationen wurden abgespeichert unter {output_dir}")

# Laufzeit berechnen
running_time = end_time - start_time

# Iteration abspeichern für Visualisierung

# Ergebnisse
print(f"Max flow: {max_flow}")
print(f"Laufzeit: {running_time} Sekunden")


# Graph abspeichern

final_network = {
    "nodes": {node_id: {"source": node.source, "target": node.target} for node_id, node in network.nodes.items()},
    "arcs": [{"start": arc.start, "end": arc.end, "capacity": arc.capacity, "flow": arc.flow} for arc in network.getArcs()]
}

output_path = f"Data/Maxflow_{input_filename}"
with open(output_path, "w") as outfile:
    json.dump(final_network, outfile)
print(f"Maxflow-Ergebnisse abgespeichert unter {output_path}")