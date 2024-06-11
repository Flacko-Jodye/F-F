# Orientiert sich an https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java

class Node:
    def __init__(self, id, source=False, target=False):
        self.id = id
        self.visited = False # Notwendig?
        self.prev = None
        self.source = source
        self.target = target