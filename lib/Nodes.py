class Node:
    def __init__(self, id, source, target):
        self.id = id
        self.visited = False # Notwendig?
        self.prev = None
        self.source = source
        self.target = target