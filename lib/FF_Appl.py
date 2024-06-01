import requests
import json
from network import Network
from Arc import Arc
from Nodes import Node
from FF import FordFulkerson

# Load the JSON data
data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_start_end.json'))

# Create a network
network = Network()

# Add nodes to the network
for node_data in data["nodes"]:
    node = Node(node_data, node_data)
    network.addNode(node)

# Add arcs to the network
for node_id in data["node"]:
    source = (node_id == "source")
    target = (node_id == "sink")
    node = Node(id= node_id, source=source, target=target)
    network.nodes[node_id] = node   



for arc_data in data["arcs"]:
    network.addArc(arc_data["start"], arc_data["end"], arc_data["capacity"])

# Calculate max flow
max_flow = FordFulkerson(network)
print(f"Max flow: {max_flow}")