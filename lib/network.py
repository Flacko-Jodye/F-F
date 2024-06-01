#To access a file from lib within lib:
#from lib.arc import Arc

# class Network:
#     def __init__(self, network_input):
#         print('TBD')

# Ergänzungen?
# - Verhinderung von möglichen overflows
# - visited token (1 oder true) oder in Nodes



class Network:
    def __init__(self):
        self.arcs = []
        self.nodes = {}

# Verschieden get-Methoden für Nodes und Arcs --> Sehr nah an: https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs
    def getSource(self):
        for arc in self.arcs:
            if arc.source == True:
                return arc
        print("Source not found")
        return None
    
    def getSink(self):
        for arc in self.arcs:
            if arc.target == True:
                return arc
        print("Target not found")
        return None
    
    def getNode(self, id):
        for node in self.arcs:
            if node.source == id:
                return node
            
    def getNodesInNetwork(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
        return False
    
    def getArcs(self):
        allArcs = []
        for node in self.network:
            for arc in self.network[node]:
                allArcs.append(arc)
        return allArcs
    
    def addEdge(self, start, end, capacity):
        # Hilfefunktionen
        if start == end:
            return "Quelle und Senke können nicht identisch sein"
        if not self.getNodesInNetwork(start):
            return "Startknoten nicht gefunden"
        if not self.getNodesInNetwork(end):
            return "Endknoten nicht gefunden"
        
        
    


    

    

        
    














# class Graph:
#     def __init__(self): # Dict/List?????
#         self.nodes = {}
#         self.arcs = []

#     def add_node(self, id, demand):
#         self.nodes[id] = Node(id, demand)

#     def add_arc(self, from_node, to_node, cost, lower_bound, upper_bound): # Nochmal demand gegenchecken
#         demand = {} 
#         if from_node not in self.nodes:
#             self.add_node(from_node, demand[from_node])
#         if to_node not in self.nodes:
#             self.add_node(to_node, demand[to_node])
#         arc = Arc(self.nodes[from_node], self.nodes[to_node], cost, lower_bound, upper_bound)
#         self.arcs.append(arc)
#         self.nodes[from_node].edges.append(arc)