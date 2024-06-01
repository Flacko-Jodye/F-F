# https://github.com/williamfiset/Algorithms/blob/master/src/main/java/com/williamfiset/algorithms/graphtheory/networkflow/FordFulkersonDFSAdjacencyMatrix.java


import json
# Load the data
with open('C:/Users/fabia/OneDrive/Dokumente/Master_FU/Semester 2/Netzwerke/F&F/F-F/Data/chvatal_small_transformed_v2.json', 'r') as infile:
    data = json.load(infile)

# Anzahl der Knoten
num_nodes = len(data['nodes'])

print(f"The number of nodes is {num_nodes}")

# Klasse erstellen

class Arc:
    def __init__(self, from_node, to_node, arc_flow, lower_bound, upper_bound, source = False, target = False):
        self.from_node = from_node # i
        self.to_node = to_node # j
        self.arc_flow = arc_flow # FLow
        self.lower_bound = lower_bound # Redundant?
        self.upper_bound = upper_bound
        self.source = source
        self.target = target



        # Für FF später
        # self.flow = 0
        # self.reverse = None