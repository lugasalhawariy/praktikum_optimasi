from pulp import * 
import pandas as pd
import numpy as np
#===========
n_warehouses = 2
n_customers = 4
# Cost Matrix
cost_matrix = np.array([[1, 3, 0.5, 4],
[2.5, 5, 1.5, 2.5]])
# Demand Matrix
cust_demands = np.array([35000, 22000, 18000, 30000])
# Supply Matrix
warehouse_supply = np.array([60000, 80000])
#===========
model = LpProblem("Supply-Demand-Problem", LpMinimize)
#===========
variable_names = [str(i)+str(j) for j in range(1, n_customers+1) for i in range(1, n_warehouses+1)]
variable_names.sort()
print("Variable Indices:", variable_names)
#===========
DV_variables = LpVariable.matrix("X", variable_names, cat = "Integer", lowBound= 0 )
allocation = np.array(DV_variables).reshape(2,4)
print("Decision Variable/Allocation Matrix: ")
print(allocation)
#===========
obj_func = lpSum(allocation*cost_matrix)
print(obj_func)
model += obj_func
print(model)
#===========
#Supply Constraints
for i in range(n_warehouses):
    # start: for(n_warehouses)
    print(lpSum(allocation[i][j] for j in range(n_customers)) <= warehouse_supply[i])
    model += lpSum(allocation[i][j] for j in range(n_customers)) <= warehouse_supply[i] , "Supply Constraints " + str(i)
    #===========
    # Demand Constraints
    for j in range(n_customers):
        print(lpSum(allocation[i][j] for i in range(n_warehouses)) >= cust_demands[j])
        model += lpSum(allocation[i][j] for i in range(n_warehouses)) >= cust_demands[j] , "Demand Constraints " + str(j)
        #===========
        model.writeLP("Supply_demand_prob.lp")
        #===========
        #model.solve()
        model.solve(PULP_CBC_CMD())
        status = LpStatus[model.status]
        print(status)
        #===========
        print("Total Cost:", model.objective.value())
        # Decision Variables
        for v in model.variables():
            try:
                print(v.name,"=", v.value())
            except:
                print("error couldnt find value")
    # end: for(n_warehouses)
# Warehouse 1 and Warehouse 2 required capacity
for i in range(n_warehouses):
    print("Warehouse ", str(i+1))
    print(lpSum(allocation[i][j].value() for j in range(n_customers)))