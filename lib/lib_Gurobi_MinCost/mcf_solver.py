import gurobipy as gp
from gurobipy import GRB
import time

def solve_mcf (nodes, arcs):
    
    model = gp.Model("min-cost-problem")

   
    model.Params.LogFile = 'gurobi_ohne_Startl.log'
    
    #Wir können die Ausgabe steuern
    model.Params.OutputFlag = 1
    model.Params.DisplayInterval = 1 
    model.Params.FeasibilityTol = 1e-9
    model.Params.OptimalityTol = 1e-9

    # Wir erstellen die Variable für den Fluss: 0<flow< capacity(lb: lower bound, ub: upper bound, name: from i to j)
    flow = {}
    for arc in arcs:
        flow[arc['from'], arc['to']] = model.addVar(
            lb=0, ub=arc['upper_bound'], name=f"flow_{arc['from']}_{arc['to']}")
            # 0<=flow<=upper_bound


    for node in nodes:
        model.addConstr(
            gp.quicksum(flow[arc['from'], arc['to']] for arc in arcs if arc['to'] == node) - gp.quicksum(flow[arc['from'], arc['to']] for arc in arcs if arc['from'] == node)==nodes[node]['demand'],
            name=f"flow_balance_{node}_in")
            #flow_in - flow_out = demand


    # Zielfunktion: hier sollen wir die gesamte Kosten minimieren.
    model.setObjective(
        gp.quicksum(flow[arc['from'], arc['to']] * arc['cost'] for arc in arcs ),
        GRB.MINIMIZE)
     #minimize sum (flow*cost)

############################### Iteration speichern########################################
#Durch die Callback-Funktion können wir die Iterationen speichern


    def my_callback(model, where):
        if where == GRB.Callback.SIMPLEX:
            iter_count = model.cbGet(GRB.Callback.SPX_ITRCNT)
            obj_val = model.cbGet(GRB.Callback.SPX_OBJVAL)
            print(f"Iteration: {iter_count}, Objective Value: {obj_val}")

            # Iterationen können dadurch gespeichert
            with open("iterations.log", "a") as f:
                f.write(f"Iteration: {iter_count}, Objective Value: {obj_val}\n")
  

        #########################################################

    model.optimize(my_callback) # Hier wird die Callback-Funktion aufgerufen und Optimierung gestartet

    if model.status == GRB.OPTIMAL: #GRB.OPTIMAL =" the optimization was successful"
        min_cost = model.objVal
        flow_values = {"arcs": [{"start": arc[0], "end": arc[1], "flow": flow[arc].X, "capacity": flow[arc].ub} for arc in flow]}
                        #  flow[arc].X = The value of the variable in the solution
        return min_cost, flow_values

    else:
        raise Exception("No optimal solution found")


    
