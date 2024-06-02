from network import Network
from Arc import Arc
from Nodes import Node

def FordFulkerson(network):
    source = network.getSource()
    sink = network.getSink()
    if source == None or sink == None:
        return "Netzwerk hat weder Quelle noch Senke"
    
    path = network.getPath(source.id, sink.id, [])
    while path is not None:
        flow = min(arc.capacity - arc.flow for arc, _ in path)
        print(f"Augmenting path found: {path} with flow {flow}")
        for arc, _ in path:
            arc.flow += flow
            arc.returnArc.flow -= flow
            print(f"Updated flow on arc from {arc.start} to {arc.end}: {arc.flow}")
        path = network.getPath(source.id, sink.id, [])
    # return sum(arc.flow for arc in network.network[source.id] if arc.end == sink.id)
    
    max_flow = sum(arc.flow for arc in network.network[source.id])
    print(f"FInale Max-FLow-Kapa der Quelle beträgt: {max_flow}")
    return max_flow

