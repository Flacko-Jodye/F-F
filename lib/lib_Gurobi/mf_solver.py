import gurobipy as gp
from gurobipy import GRB




def solve_mf (nodes, arcs, source, sink):
    model = gp.Model("max_flow")

    # Gurobi log file
    model.Params.LogFile = 'mf_gurobi.log'
    
    # Hird können wir die Ausgabe steuern
    model.Params.OutputFlag = 1
    model.Params.DisplayInterval = 1 
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9

    # Hier erstellen wir Flowvalue : 0<flow< capacity(lb: lower bound, ub: upper bound/capacity, name: from i to j)
    flow = {}
    for arc in arcs:
        flow[arc['start'], arc['end']] = model.addVar(
            lb=0, ub=arc['capacity'], name=f"flow_{arc['start']}_{arc['end']}")
        
        
    # constraints        
    for node in nodes:
        if node == source:
                
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) == 0,
                name=f"flow_balance_{node}_in")
                #Für "Source": die Summe der Flüsse, die in die Quelle fließen, ist 0
                            
        elif node == sink:

            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node) == 0,
                name=f"flow_balance_{node}_out")
                #Für "Sink": die Summe der Flüsse, die aus der Senke fließen, ist 0

        else:
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) ==
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node),
                name=f"flow_balance_{node}")
                #Für alle anderen Knoten: die Summe der Flüsse, die in den Knoten fließen, ist gleich der Summe der Flüsse, die aus dem Knoten fließen
    
    
    # Zielfunktion: Maximierung des Flusses, der in die Senke fließt
    model.setObjective(
        gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == sink),
        GRB.MAXIMIZE)
    
    
    
    ############################### Iteration speichern########################################
    # Nur wenn wir die Callback-Funktion verwenden, können wir die Iterationen speichern

    def my_callback(model, where):
        if where == GRB.Callback.SIMPLEX:
            iter_count = model.cbGet(GRB.Callback.SPX_ITRCNT)
            obj_val = model.cbGet(GRB.Callback.SPX_OBJVAL)
            print(f"Iteration: {iter_count}, Objective Value: {obj_val}")

            # Hier speichern wir jede Iterationen in eine Datei

            with open("mf_iterations_gurobi.log", "a") as f:
                f.write(f"Iteration: {iter_count}, Objective Value: {obj_val}\n")
                
    ###############################################################################################


    model.optimize(my_callback)


    if model.status == GRB.OPTIMAL: #GRB.OPTIMAL =" the optimization was successful"
        max_flow = model.objVal
        flow_values = {"arcs": [{"start": arc[0], "end": arc[1], "flow": flow[arc].X, "capacity": flow[arc].ub} for arc in flow]}
                            #  flow[arc].X = hier wird der Wert des Flusses zurückgegeben, damit wir wissen, wie viel Fluss durch die Kante fließt
        return max_flow, flow_values
    else:
        raise Exception("No optimal solution found")
    