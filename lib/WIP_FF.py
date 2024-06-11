# 3 verschieden Modi für Ford-Fulkerson Algorithmus
    # 1. FordFulkerson_Flow: Berechnet den maximalen Fluss und gibt diesen zurück. Es werden keine Zwischenschritte ausgegeben. Ziel: Maximale Flussberechnung in kürzester Zeit.
    # 2. FordFulkerson_Debug: Berechnet den maximalen Fluss und gibt Zwischenschritte aus. Ziel: Verständnis des Algorithmus.
    # 3. FordFulkerson_Graph: Berechnet den maximalen Fluss und speichert Zwischenschritte als JSON-Dateien ab. Ziel: Visualisierung des Algorithmus.

# Ausführung der Modi in den jeweiligen Apply-Dateien

from network import Network
from Arc import Arc
from Nodes import Node
import json
import os
import random

# s-t-Schnitt ausgeben
def find_st_cut(network, source):
    visited = set()
    stack = [source]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for arc in network.network[node]:
                if arc.capacity - arc.flow > 0 and arc.end not in visited:
                    stack.append(arc.end)
    return visited



def FordFulkerson_Flow(network, log_core_usage):
    source = network.getSource()
    sink = network.getSink()
    if source is None or sink is None:
        return "Netzwerk hat weder Quelle noch Senke"

    def flussErhoehen_path(source, sink):
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
                        return new_path
                    stack.append((arc.end, new_path))
        return None

    max_flow = 0
    iterations = 0 # Iterationen zählen
    path = flussErhoehen_path(source.id, sink.id)
    while path is not None:
        flow = min(residual_capacity for arc, residual_capacity in path)
        for arc, _ in path:
            arc.flow += flow
            arc.returnArc.flow -= flow
        max_flow += flow

        iterations += 1 # Löuft er noch?
        if iterations % 1000 == 0:
            print(f"Iteration {iterations}")
            # print(max_flow)

        log_core_usage()
        path = flussErhoehen_path(source.id, sink.id)

    s_cut = find_st_cut(network, source.id)
    t_cut = set(network.nodes.keys()) - s_cut

    return max_flow, iterations, s_cut, t_cut



def FordFulkerson_Debug(network, log_core_usage):
    source = network.getSource()
    sink = network.getSink()
    if source is None or sink is None:
        return "Netzwerk hat weder Quelle noch Senke"

    def flussErhoehen_path(source, sink):
        visited = set()
        stack = [(source, [])]
        iteration = 0 # Debugging

        while stack:
            current_node, path = stack.pop()
            if current_node in visited:
                continue
            visited.add(current_node)

            # # Für 3. Instanz des Extrembeispiels --> Unterschiede zwischen
            # # neighbors = [(arc, arc.capacity - arc.flow) for arc in network.network[current_node] if (arc.capacity - arc.flow) > 0 and arc.end not in visited]
            # neighbors = [(arc, arc.capacity - arc.flow) for arc in network.network[current_node] if arc.end not in visited]
            # # Shufflen um Reihenfolge zu verändern
            # random.shuffle(neighbors)

            # print(f"Iteration {iteration}: Exploring neighbors of {current_node}") # Debugging
            # # for arc in network.network[current_node]:
            # for arc, residual_capacity in neighbors:
            for arc in network.network[current_node]:
                print(f"  Considering arc {arc.start} -> {arc.end} with residual capacity {residual_capacity}") # Debugging
                residual_capacity = arc.capacity - arc.flow
                if residual_capacity > 0 and arc.end not in visited:
                    new_path = path + [(arc, residual_capacity)]
                    if arc.end == sink:
                        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in new_path])
                        print(f"Pfad zur Senke gefunden: {path_str}")
                        return new_path
                    stack.append((arc.end, new_path))

            # Shuffle the stack to ensure different path selection order
            print(f"Stack before shuffling: {stack}")
            random.shuffle(stack)  # Shuffle the stack to ensure random path selection order
            print(f"Stack after shuffling: {stack}")

        print("Kein flussvergrößernder Pfad gefunden")
        return None

    max_flow = 0
    iterations = 0
    path = flussErhoehen_path(source.id, sink.id)
    while path is not None:
        flow = min(residual_capacity for arc, residual_capacity in path)
        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in path])
        print(f"Flussvergrößernder Pfad gefunden: {path_str} mit Fluss {flow}")
        for arc, _ in path:
            arc.flow += flow
            arc.returnArc.flow -= flow
            print(f"Aktualisierter Fluss auf Kante von {arc.start} nach {arc.end}: {arc.flow}")
            print(f"Aktualisierter Fluss auf Rückwärtskante von {arc.end} nach {arc.start}: {arc.returnArc.flow}")
        max_flow += flow

        # Kernauslastung tracken
        log_core_usage()

        iterations += 1

        path = flussErhoehen_path(source.id, sink.id)

    print(f"Endgültiger maximaler Fluss: {max_flow}")
    s_cut = find_st_cut(network, source.id)
    t_cut = set(network.nodes.keys()) - s_cut

    return max_flow, iterations, s_cut, t_cut



def FordFulkerson_Graph(network, output_dir, log_core_usage):
    source = network.getSource()
    sink = network.getSink()
    if source is None or sink is None:
        return "Netzwerk hat weder Quelle noch Senke"

    def flussErhoehen_path(source, sink):
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
                        return new_path
                    stack.append((arc.end, new_path))
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
    iteration = 0 # Für die Graphenvisualisierung

    iterations = 0 # Iterationen zählen

    max_flow = 0
    path = flussErhoehen_path(source.id, sink.id)
    while path is not None:
        flow = min(residual_capacity for arc, residual_capacity in path)
        for arc, _ in path:
            arc.flow += flow # Fluss des Pfads erhöhen
            arc.returnArc.flow -= flow  # Rückwärtskante aktualisieren
        max_flow += flow

        # Iteration des Graphens abspeichern
        save_network_iteration(network, iterations, path, output_dir)
        iterations += 1

        
        # Kernauslastung tracken
        log_core_usage()

        path_str = " -> ".join([f"{arc.start}->{arc.end} (Restkapazität: {residual_capacity})" for arc, residual_capacity in path])
        print(f"Iteration {iterations}: Augmenting path: {path_str}, Flow added: {flow}, Max flow so far: {max_flow}")
        

        path = flussErhoehen_path(source.id, sink.id)
    s_cut = find_st_cut(network, source.id)
    t_cut = set(network.nodes.keys()) - s_cut
    print(f"Final Max flow: {max_flow}")
    return max_flow, iterations, s_cut, t_cut