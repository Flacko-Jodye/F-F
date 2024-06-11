# Generelle Struktur nah an: https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs sowie https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java
# Ergänzungen zum Schluss von ChatGPT (s. letzte Zeilen)
from lib.Arc import Arc

class Network:
    def __init__(self):
        self.arcs = []
        self.nodes = {}
        self.network = {}

# Verschieden get-Methoden für Nodes und Arcs --> Sehr nah an: https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs
    #.values von ChatGPT übernommen --> Nochmal recherchieren
    def getSource(self):
        for node in self.nodes.values():
            print(f"Checking node {node.id}: source={node.source}")  # Debugging
            if node.source == True:
                return node
        print("Source not found")
        return None
    
    def getSink(self):
        for node in self.nodes.values():
            print(f"Checking node {node.id}: sink ={node.target}")  # Debug statement
            if node.target == True:
                return node
        print("Sink not found")
        return None

    def getNode(self, id):
        return self.nodes.get(id)
    
    def getNodesInNetwork(self, id):
        return id in self.nodes

    def getArcs(self):
        allArcs = []
        for arcs in self.network.values():
            allArcs.extend(arcs)
        return allArcs

        
    def getPath(self, start, end, path):
        if start == end:
            return path # Pfad gefunden
        for arc in self.network.get(start, []):
            residualCapacity = arc.capacity - arc.flow
            if residualCapacity > 0 and not (arc, residualCapacity) in path:
                print(f"Exploring arc from {arc.start} to {arc.end} with residual capacity {residualCapacity}")
                result = self.getPath(arc.end, end, path + [(arc, residualCapacity)])
                if result is not None:
                    return result 
        return None

    def addArc(self, start, end, capacity):
    # Hilfefunktionen
        # if start == end:
        #     return "Quelle und Senke können nicht identisch sein"
        # if not self.getNodesInNetwork(start):
        #     return "Startknoten nicht gefunden"
        # if not self.getNodesInNetwork(end):
        #     return "Endknoten nicht gefunden"
        if start == end:
            raise ValueError("Quelle und Senke können nicht identisch sein")
        if not self.getNodesInNetwork(start):
            raise ValueError(f"Startknoten {start} nicht gefunden")
        if not self.getNodesInNetwork(end):
            raise ValueError(f"Endknoten {end} nicht gefunden")
        
        newArc = Arc(start, end, capacity)
        returnArc = Arc(end, start, 0)
        newArc.returnArc = returnArc
        returnArc.returnArc = newArc

        if start not in self.network:
            self.network[start] = []

        if end not in self.network:
            self.network[end] = []
        node = self.getNode(start) # Startknoten
        returnNode = self.getNode(end) # Endknoten
        self.network[node.id].append(newArc)
        self.network[returnNode.id].append(returnArc)  

        # ChatGPT Ergänzungen
        self.arcs.append(newArc)
        self.arcs.append(returnArc)
        print(f"Pfad hinzugefügt von {start} zu {end} mit Kapazität {capacity}")
        print(f"Pfad hinzugefügt von {end} zu {start} mit Kapazität 0")
