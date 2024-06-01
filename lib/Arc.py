# https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java


import json
# Load the data
with open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/transformed_chvatal_small.json', 'r') as infile:
    data = json.load(infile)

# Anzahl der Knoten
num_nodes = len(data['nodes'])

print(f"The number of nodes is {num_nodes}")

# Klasse erstellen

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


        # Für FF später
        # self.flow = 0
        # self.reverse = None