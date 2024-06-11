# Struktur orientiert sich an https://brilliant.org/wiki/ford-fulkerson-algorithm/#residual-graphs
    # Vergleich mit https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java 

class Arc:
    def __init__(self, start, end, capacity):
        self.start = start # i
        self.end = end # j
        self.capacity = capacity # Maximal möglicher FLow (Konstant) / != 0
                                 # Residualkapazität muss =0 sein
        # self.lower_bound = lower_bound # Redundant?
        # self.upper_bound = upper_bound
        self.flow = 0 # (dynamisch)
        self.return_arc = None


