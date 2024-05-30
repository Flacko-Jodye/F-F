class Node:
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand
        self.edges = []
        self.visited = False # Notwendig?
        self.cost = 0 # Wahrscheinlich irrelevant
        self.prev = None