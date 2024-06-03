from network import Network
from Arc import Arc
from Nodes import Node

def FordFulkerson(network):
    source = network.getSource()
    sink = network.getSink()
    if source is None or sink is None:
        return "Netzwerk hat weder Quelle noch Senke"

    def flussErhoehen_path(source, sink):
        visited = set()
        stack = [(source, [])]

# Stack als Ergänzung
        while stack:
            current_node, path = stack.pop()
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
                    stack.append((arc.end, new_path))
        print("Kein flussvergrößernder Pfad gefunden")
        return None

    max_flow = 0
    path = flussErhoehen_path(source.id, sink.id)
    while path is not None:
        flow = min(residual_capacity for arc, residual_capacity in path)
        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in path])
        print(f"Flussvergrößernder Pfad gefunden: {path_str} mit Fluss {flow}")
        for arc, _ in path:
            arc.flow += flow
            arc.returnArc.flow -= flow  # Rückwärtskante aktualisieren
            print(f"Aktualisierter Fluss auf Kante von {arc.start} nach {arc.end}: {arc.flow}")
            print(f"Aktualisierter Fluss auf Rückwärtskante von {arc.end} nach {arc.start}: {arc.returnArc.flow}")
        max_flow += flow
        print(f"Aktueller maximaler Fluss: {max_flow}")
        path = flussErhoehen_path(source.id, sink.id)

    print(f"Endgültiger maximaler Fluss: {max_flow}")
    return max_flow
