# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:02:23 2022

@author: iainh
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:15:00 2022

@author: iainh
"""

from ortools.sat.python import cp_model

model = cp_model.CpModel()

cost = [[1,2],[3,4],[5,6]]
downtime = [-1, -3, -4]
demand  = [1, 2, 3]

num_cost = 2
num_choice = 3
num_action = 3

all_cost  = range(num_cost)
all_choice = range(num_choice)
all_task = range(num_action)
action = {}

for a in all_task:
    for b in all_choice:
        action[(a,b)] = model.NewBoolVar('task%i choice%i' % (a,b))
        
for a in all_task:    
    model.AddExactlyOne(action[(a,b)] for b in all_cost)

active = {}
for a in all_task:
    active  = model.NewBoolVar('demand active at %i' % a)


model.AddExactlyOne(action[(a,2)] for a in all_task)

t = [0,1,2]
model.AddReservoirConstraintWithActive(t[1], demand[1], active[1], 0 , 4)




model.Minimize(sum( sum(action[(a,b)] * cost[a][b] for b in all_cost) + action[(a,2)] * downtime[a]  for a in all_task )  )

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print('Solution:')
    totalCost = 0
    for a in all_task:
        print('action', a)
        for b in all_cost:
            if solver.Value(action[(a,b)]) == 1:
                print('Choice %i chosen, cost %i' % (b, cost[a][b]))
                totalCost = totalCost + cost[a][b]
            else:
                print('Choice %i not chosen' % b)
        if solver.Value(action[(a,b+1)]) == 1:
            print('Downtime chosen, cost %i ' % downtime[a] )
            totalCost = totalCost+downtime[a]
        else:
            print('Downtime not chosen')
    print('total cost %i' % totalCost)
    print(f'total cost = {solver.ObjectiveValue()}' )
else:
    print('No optimal solution found !')



'''
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True








class PartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, action, num_cost, num_action, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._action = action
        self._num_cost = num_cost
        self._num_action = num_action
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print('Solution %i' % self._solution_count)
        totalCost = 0
        for a in range(self._num_action):
            print('Action %i' % a)
            for b in range(self._num_cost):
                
                if self.Value(self._action[(a,b)]):
                    print('Choice %i chosen, cost %i' % (b, cost[a][b]))
                    totalCost = totalCost + cost[a][b]
                else:
                    print('Choice %i not chosen' % b)
        print('total cost of actions is %i' % totalCost)
        if self._solution_count >= self._solution_limit:
            print('Stop search after %i solutions' % self._solution_limit)
            self.StopSearch()
            
    def solution_count(self):
        return self._solution_count

# Display the first five solutions.
solution_limit = 2
solution_printer = PartialSolutionPrinter(action, num_cost, num_action, solution_limit)


solver.Solve(model, solution_printer)

'''