#To access a file from lib within lib:
#from lib.arc import Arc

class Network:
    def __init__(self, network_input):
        print('TBD')


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