# Min-Cost with Dijkstra's Algorithm

import json
import heapq
# Für die Visualisierung des Graphen
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand
        self.edges = []
        self.visited = False # Notwendig?
        self.cost = 0 # ?
        self.prev = None
class Arc:
    def __init__(self, from_node, to_node, cost, lower_bound, upper_bound):
        self.from_node = from_node # i
        self.to_node = to_node # j
        self.cost = cost # bzw. Distanz
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        # Für FF später
        # self.flow = 0
        # self.reverse = None

# https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs
class Graph:
    def __init__(self): # Dict/List?????
        self.nodes = {}
        self.arcs = []

    def add_node(self, id, demand):
        self.nodes[id] = Node(id, demand)

    def add_arc(self, from_node, to_node, cost, lower_bound, upper_bound): # Nochmal demand gegenchecken
        demand = {} 
        if from_node not in self.nodes:
            self.add_node(from_node, demand[from_node])
        if to_node not in self.nodes:
            self.add_node(to_node, demand[to_node])
        arc = Arc(self.nodes[from_node], self.nodes[to_node], cost, lower_bound, upper_bound)
        self.arcs.append(arc)
        self.nodes[from_node].edges.append(arc)


# Hier nochmal nachfragen ob Dijkstra oder doch Simplex/Primal-Dual
# Erfüllt noch nicht die Bedingungen für Angebot und Bedarf
    def dijkstra(self, start_node, end_node):
        start_node = self.nodes[start_node]
        end_node = self.nodes[end_node]
        start_node.cost = 0

        queue = [(0, start_node)]
        while queue:
            _, current_node = heapq.heappop(queue)

            if current_node.visited:
                continue

            if current_node == end_node:
                break

            current_node.visited = True
            for arc in current_node.edges:
                neighbor = self.nodes[arc.to_node.id]  # Use arc.to_node.id instead of arc.to_node
                new_cost = current_node.cost + arc.cost

                if new_cost < neighbor.cost:
                    neighbor.cost = new_cost
                    neighbor.prev = current_node
                    heapq.heappush(queue, (new_cost, neighbor))

                                # Check if the new cost satisfies the demand and does not surpass the upper bound
                # if new_cost < neighbor.cost and new_cost >= neighbor.demand and new_cost <= arc.upper_bound:
                #     neighbor.cost = new_cost
                #     heapq.heappush(queue, (new_cost, neighbor))
    
# JSON laden / Graph erstellen
# with open("chvatal_small.json") as data_source:
#     data = json.load(data_source)

data = json.load(open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/Netzwerke1/Vorlage_Projekt_Netzwerke/Data/chvatal_small.json'))

graph = Graph()

for id, info in data["nodes"].items():
    graph.add_node(id, info["demand"])

for arc in data["arcs"]:
    graph.add_arc(arc["from"], arc["to"], arc["cost"], arc["lower_bound"], arc.get("upper_bound", float('inf')))

nodes = list(graph.nodes.keys())
for start_node in nodes:
    for end_node in nodes:
        if start_node != end_node:
            graph.dijkstra(start_node, end_node)



'spätere Referenz: https://www.geeksforgeeks.org/ford-fulkerson-algorithm-in-python/'


# # Create a new graph
G = nx.DiGraph()

# Add nodes to the graph
node_labels = {}
for node in graph.nodes.values():
    G.add_node(node.id)
    node_labels[node.id] = node.demand  # Assuming the demand is stored in the node

# Add edges to the graph
edge_labels = {}
for arc in graph.arcs:
    G.add_edge(arc.from_node.id, arc.to_node.id)
    upper_bound = arc.upper_bound if arc.upper_bound != float("inf") else "inf"
    edge_labels[(arc.from_node.id, arc.to_node.id)] = f'{arc.cost}, {arc.lower_bound}, {upper_bound}'

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, arrows= True, edge_color = "blue", node_color = "red", node_size = 500, font_size = 10, font_color = "white")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Draw node names within the nodes
nx.draw_networkx_labels(G, pos, font_color = "white")

# Adjust label positions for demand values
label_pos = {node: (coords[0], coords[1] + 0.1) for node, coords in pos.items()}
nx.draw_networkx_labels(G, label_pos, labels=node_labels, font_color = "black")

plt.show()