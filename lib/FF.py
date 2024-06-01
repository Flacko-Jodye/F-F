from network import Network
from Arc import Arc
from Nodes import Node

def FordFulkerson(network):
    source = network.getSource()
    sink = network.getSink()
    if source == None or sink == None:
        return "Netzwerk hat weder Quelle noch Senke"
    
    path = network.getPath(source.id, sink.id, [])
    while path != None:
        flow = min(arc.capacity - arc.flow for arc in path)
        for arc, _ in path:
            arc.flow += flow
            arc.returnArc.flow -= flow
        path = network.getPath(source.id, sink.id, [])
    return sum(arc.flow for arc in network.network[source.id] if arc.end == sink.id)

