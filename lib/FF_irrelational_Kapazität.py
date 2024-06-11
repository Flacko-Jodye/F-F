import math
from network import Network
from Arc import Arc
from Nodes import Node
import json
import os

def FordFulkerson(network, output_dir):
    source = network.getSource()
    sink = network.getSink()
    if source is None or sink is None:
        return "Netzwerk hat weder Quelle noch Senke"

    def fluss_erhoehen_path(source, sink):
        visited = set()
        stack = [(source, [])]

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

    def save_network_iteration(network, iteration, augmenting_path, output_dir):
        state = {
            "nodes": {node_id: {"source": node.source, "target": node.target} for node_id, node in network.nodes.items()},
            "arcs": [{"start": arc.start, "end": arc.end, "capacity": arc.capacity, "flow": arc.flow} for arc in network.getArcs() if arc.flow > 0],  # Store only positive flow arcs
            "augmenting_path": [(arc.start, arc.end) for arc, _ in augmenting_path]
        }
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f"network_{iteration}.json"), "w") as outfile:
            json.dump(state, outfile)
    
    
    iteration = 0
    max_flow = 0
    path = fluss_erhoehen_path(source.id, sink.id)
    
    an = 1
    an_plus_1 = math.pi

    while path is not None:
        if iteration % 2 == 0:
            flow = an
        else:
            flow = an_plus_1

        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in path])
        print(f"Flussvergrößernder Pfad gefunden: {path_str} mit Fluss {flow}")
        for arc, _ in path:
            arc.flow += flow  # 增加路径上的流量
            arc.returnArc.flow -= flow  # 更新反向边上的流量
            print(f"Aktualisierter Fluss auf Kante von {arc.start} nach {arc.end}: {arc.flow}")
            print(f"Aktualisierter Fluss auf Rückwärtskante von {arc.end} nach {arc.start}: {arc.returnArc.flow}")

        max_flow += flow
        print(f"Aktueller maximaler Fluss: {max_flow}")

        # 更新递归序列
        an, an_plus_1 = an_plus_1, an - an_plus_1

        save_network_iteration(network, iteration, path, output_dir)
        iteration += 1

        path=fluss_erhoehen_path(source.id, sink.id)

    print(f"Endgültiger maximaler Fluss: {max_flow}")
    return max_flow




"Alte Version"

# from network import Network
# from Arc import Arc
# from Nodes import Node

# def FordFulkerson(network):
#     source = network.getSource()
#     sink = network.getSink()
#     if source is None or sink is None:
#         return "Netzwerk hat weder Quelle noch Senke"

#     def flussErhoehen_path(source, sink):
#         visited = set()
#         stack = [(source, [])]

# # Stack als Ergänzung --> ChatGPT Ergänzung
#         while stack:
#             current_node, path = stack.pop()
#             if current_node in visited:
#                 continue
#             visited.add(current_node)

#             for arc in network.network[current_node]:
#                 residual_capacity = arc.capacity - arc.flow
#                 if residual_capacity > 0 and arc.end not in visited:
#                     new_path = path + [(arc, residual_capacity)]
#                     if arc.end == sink:
#                         path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in new_path])
#                         print(f"Pfad zur Senke gefunden: {path_str}")
#                         return new_path
#                     stack.append((arc.end, new_path))
#         print("Kein flussvergrößernder Pfad gefunden")
#         return None

#     max_flow = 0
#     path = flussErhoehen_path(source.id, sink.id)
#     while path is not None:
#         flow = min(residual_capacity for arc, residual_capacity in path)
#         path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in path])
#         print(f"Flussvergrößernder Pfad gefunden: {path_str} mit Fluss {flow}")
#         for arc, _ in path:
#             arc.flow += flow # Fluss des Pfads erhöhen
#             arc.returnArc.flow -= flow  # Rückwärtskante aktualisieren
#             print(f"Aktualisierter Fluss auf Kante von {arc.start} nach {arc.end}: {arc.flow}")
#             print(f"Aktualisierter Fluss auf Rückwärtskante von {arc.end} nach {arc.start}: {arc.returnArc.flow}")
#         # Gesamtflow berechnen und ausgeben
#         max_flow += flow
#         print(f"Aktueller maximaler Fluss: {max_flow}")
#         path = flussErhoehen_path(source.id, sink.id)

#     print(f"Endgültiger maximaler Fluss: {max_flow}")
#     return max_flow