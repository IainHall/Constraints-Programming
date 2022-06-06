# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 15:30:28 2022

@author: iainh

trying to create a constraint programming problem and solve it
"""

from ortools.sat.python import cp_model

model = cp_model.CpModel()

num_house = 6
num_postmen= 2
all_house = range(num_house)
all_postmen = range(num_postmen)
parcels = {}


# boolean array representing whether a postman gives a parcel to a house
for p in all_postmen:
    for h in all_house:
        parcels[(p,h)] = model.NewBoolVar('parcel_p%ih%i' % (p, h))
        
        
#Makes it so each postman can only service one house
for h in all_house:
    model.AddExactlyOne(parcels[(p,h)] for p in all_postmen)
    
min_parcels = num_house//num_postmen
if num_house % num_postmen == 0 :
    max_parcels = min_parcels
else:
    max_parcels = min_parcels + 1

for p in all_postmen:
    num_parcels_delivered = []
    for h in all_house:
        num_parcels_delivered.append(parcels[(p,h)])
        
    model.Add(min_parcels <= sum(num_parcels_delivered))
    model.Add(sum(num_parcels_delivered) <= max_parcels)
    
    
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True


class PostmenPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, parcels, num_postmen, num_house, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._parcels = parcels
        self._num_postmen = num_postmen
        self._num_house = num_house
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print('Solution %i' % self._solution_count)
        for p in range(self._num_postmen):
            for h in range(self._num_house):
                if self.Value(self._parcels[(p, h)]):
                    print('  Postman %i delivers parcel to house %i' % (p, h))
        if self._solution_count >= self._solution_limit:
            print('Stop search after %i solutions' % self._solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self._solution_count

# Display the first five solutions.
solution_limit = 5
solution_printer = PostmenPartialSolutionPrinter(parcels, num_postmen,
                                                num_house,
                                                solution_limit)
        
        
        
        
        
        
        
        
        