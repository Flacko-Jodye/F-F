from network import Network
from Arc import Arc
from Nodes import Node
from collections import deque

def FordFulkerson(network):
    source = network.getSource()
    sink = network.getSink()
    if source is None or sink is None:
        return "Netzwerk hat weder Quelle noch Senke"

    def bfs(source, sink):
        visited = set()
        queue = deque([(source, [])])
        # Queue here: besuchen immer zuerst den am längsten in der Warteschlange stehenden Knoten, um sicherzustellen, 
                    # dass wir immer zuerst die Knoten besuchen, die näher an der Quelle liegen.
        while queue:
            current_node, path = queue.popleft()
            if current_node in visited:
                continue
            visited.add(current_node)

            for arc in network.network[current_node]:
                residual_capacity = arc.capacity - arc.flow
                if residual_capacity > 0 and arc.end not in visited:
                    new_path = path + [(arc, residual_capacity)]
                    if arc.end == sink:
                        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in new_path])
                        print(f"Pfad zur Senke gefunden: {path_str}")
                        return new_path
                    queue.append((arc.end, new_path))
        print("Kein flussvergrößernder Pfad gefunden")
        return None

    max_flow = 0
    path = bfs(source.id, sink.id)
    while path is not None:
        flow = min(residual_capacity for arc, residual_capacity in path)
        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in path])
        print(f"Flussvergrößernder Pfad gefunden: {path_str} mit Fluss {flow}")
        for arc, _ in path:
            arc.flow += flow
        max_flow += flow
        path = bfs(source.id, sink.id)


    return max_flow