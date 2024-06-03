import gurobipy as gp
from gurobipy import GRB




def solve_mf (nodes, arcs, source, sink):
    model = gp.Model("max_flow")

    # Set Gurobi log file
    model.Params.LogFile = 'gurobi.log'
    
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
        
        # addVar: add a new variable to the model(1b: lower bound, ub: upper bound, obj: objective coefficient, vtype: variable type, name: variable name)

    #constraints        
    for node in nodes:
        if node == source:
                
            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['end'] == node) == 0,
                name=f"flow_balance_{node}_in")
                #for source: each flow out <= sum of capacity
                            #sum of flow in = 0
        elif node == sink:

            model.addConstr(
                gp.quicksum(flow[arc['start'], arc['end']] for arc in arcs if arc['start'] == node) == 0,
                name=f"flow_balance_{node}_out")
            #for sink: each flow in <= sum of capacity
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
    ############################### Iteration speichern########################################
    def my_callback(model, where):
        if where == GRB.Callback.SIMPLEX:
            iter_count = model.cbGet(GRB.Callback.SPX_ITRCNT)
            obj_val = model.cbGet(GRB.Callback.SPX_OBJVAL)
            print(f"Iteration: {iter_count}, Objective Value: {obj_val}")
            # Write each iteration's information to a file
            with open("iterations.log", "a") as f:
                f.write(f"Iteration: {iter_count}, Objective Value: {obj_val}\n")


        #########################################################
    '''# Check if the model is infeasible
    if model.status == GRB.Status.INFEASIBLE:
        print('The model is infeasible; computing IIS')

    # Compute IIS
    model.computeIIS()
    print('\nThe following constraint(s) cannot be satisfied:')
    for c in model.getConstrs():
        if c.IISConstr:
            print('%s' % c.constrName)
    
    

    '''
        ########################################
    # Solve the model with the callback function
    model.optimize(my_callback)

    if model.status == GRB.OPTIMAL: #GRB.OPTIMAL =" the optimization was successful"
        max_flow = model.objVal
        flow_values = {arc: flow[arc].X for arc in flow}
                        #  flow[arc].X = flow value of each arc
        return max_flow, flow_values
    else:
        raise Exception("No optimal solution found")
    