import gurobipy as gp
from gurobipy import GRB




def solve_mf (nodes, arcs, source, sink):
    model = gp.Model("max_flow")

    # Set Gurobi log file
    model.Params.LogFile = 'mf_gurobi.log'
    
    # Enable verbose output
    model.Params.OutputFlag = 1
    model.Params.DisplayInterval = 1 
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9

    # create variable for flow : 0<flow< capacity
    flow = {}
    for arc in arcs:
        flow[arc['start'], arc['end']] = model.addVar(
            lb=0, ub=arc['capacity'], name=f"flow_{arc['start']}_{arc['end']}")
        
        
    #constraints        
    for node in nodes:
        if node == source:
                
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) == 0,
                name=f"flow_balance_{node}_in")
                #for source: 
                            #sum of flow in = 0
        elif node == sink:

            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node) == 0,
                name=f"flow_balance_{node}_out")
                #for sink: 
                            #flow out = flow from source to other nodes
        else:
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) ==
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node),
                name=f"flow_balance_{node}")
    
    
    
    # Set objective
    model.setObjective(
        gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == sink),
        GRB.MAXIMIZE)
    model.optimize(my_callback)
    
    ############################### Iteration speichern########################################
    def my_callback(model, where):
        if where == GRB.Callback.SIMPLEX:
            iter_count = model.cbGet(GRB.Callback.SPX_ITRCNT)
            obj_val = model.cbGet(GRB.Callback.SPX_OBJVAL)
            print(f"Iteration: {iter_count}, Objective Value: {obj_val}")
            # Write each iteration's information to a file
            with open("mf_iterations_gurobi.log", "a") as f:
                f.write(f"Iteration: {iter_count}, Objective Value: {obj_val}\n")
    ############################################################################################
    
    if model.status == GRB.OPTIMAL: 
        max_flow = model.objVal
        flow_values = {"arcs": [{"start": arc[0], "end": arc[1], "flow": flow[arc].X, "capacity": flow[arc].ub} for arc in flow]}
                        #  flow[arc].X = flow value of each arc
        return max_flow, flow_values
    else:
        raise Exception("No optimal solution found")
    