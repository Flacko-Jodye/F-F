class Node:
    def __init__(self, id, source=False, target=False):
        self.id = id
        self.visited = False # Notwendig?
        self.prev = None
        self.source = source
        self.target = target