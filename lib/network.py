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
        self.network = {}

# Verschieden get-Methoden für Nodes und Arcs --> Sehr nah an: https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs
    #.values von ChatGPT übernommen --> Nochmal recherchieren
    def getSource(self):
        for node in self.nodes.values():
            if node.source == True:
                return node
        print("Source not found")
        return None
    
    def getSink(self):
        for node in self.nodes.values():
            if node.target == True:
                return node
        print("Target not found")
        return None
    
    # def getNode(self, id):
    #     for node in self.arcs:
    #         if node.source == id:
    #             return node

    def getNode(self, id):
        return self.nodes.get(id)
    
            
    # def getNodesInNetwork(self, id):
    #     for node in self.nodes:
    #         if node.id == id:
    #             return node
    #     return False
    
    def getNodesInNetwork(self):
        return id in self.nodes

    def getArcs(self):
        allArcs = []
        for node in self.network:
            for arc in self.network[node]:
                allArcs.append(arc)
        return allArcs

        
    def getPath(self, start, end, path):
        if start == end:
            return path # Pfad gefunden
        for arc in self.network.get[start, []]:
            residualCapacity = arc.capacity - arc.flow
            if residualCapacity > 0 and not (arc, residualCapacity) in path:
                result = self. getPath(arc.end, end, path + [(arc, residualCapacity)])
                if result is not None:
                    return result 

    def addArc(self, start, end, capacity):
    # Hilfefunktionen
        if start == end:
            return "Quelle und Senke können nicht identisch sein"
        if not self.getNodesInNetwork(start):
            return "Startknoten nicht gefunden"
        if not self.getNodesInNetwork(end):
            return "Endknoten nicht gefunden"
        newArc = Arc(start, end, capacity)
        returnArc = Arc(end, start, 0)
        newArc.returnArc = returnArc
        returnArc.returnArc = newArc
        if start not in self.network:
            self.network[start] = []
        if end not in self.network:
            self.network[end] = []
        node = self.getNode(start) # Startknoten
        returnNode = self.getNode(end)
        self.network[node.id].append(newArc)
        self.network[returnNode.id].append(returnArc)  

        # ChatGPT Ergänzungen
        self.arcs.append(newArc)
        self.arcs.append(returnArc)
