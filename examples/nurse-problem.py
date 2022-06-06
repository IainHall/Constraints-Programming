# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the cript file for learning how to use google OR tools for optimisiing
the nurse scheduling problem
"""

from ortools.sat.python import cp_model

num_nurses = 5
num_shifts = 3
num_days = 7
all_nurses = range(num_nurses)
all_shifts = range(num_shifts)
all_days = range(num_days)
shift_requests = [[[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1],
                   [0, 1, 0], [0, 0, 1]],
                  [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],
                   [0, 0, 0], [0, 0, 1]],
                  [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],
                   [0, 1, 0], [0, 0, 0]],
                  [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],
                   [1, 0, 0], [0, 0, 0]],
                  [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],
                   [0, 1, 0], [0, 0, 0]]]

model = cp_model.CpModel()


#creates a boolean array of all the possible assignments, with a value of 1 if actually assigned
shifts = {}
for n in all_nurses:
    for d in all_days:
        for s in all_shifts:
            shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))
            

# constraint that the number of nurses assigned to work a shift is 1
for d in all_days:
    for s in all_shifts:
        model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)
     
# the sum of shifts that can be assigned to each nurse for each day is limited to 1
for n in all_nurses:
    for d in all_days:
        model.AddAtMostOne(shifts[(n, d, s)] for s in all_shifts)
        
        
        
# Try to distribute the shifts evenly, so that each nurse works
# min_shifts_per_nurse shifts. If this is not possible, because the total
# number of shifts is not divisible by the number of nurses, some nurses will
# be assigned one more shift.
min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
if num_shifts * num_days % num_nurses == 0:
    max_shifts_per_nurse = min_shifts_per_nurse   #minimum number of shits each nurse must work
else:
    max_shifts_per_nurse = min_shifts_per_nurse + 1   #maximum number of shifts each nurse must work
for n in all_nurses:
    num_shifts_worked = []
    for d in all_days:
        for s in all_shifts:
            num_shifts_worked.append(shifts[(n, d, s)])
    #constraint that each nurse must work at least the minimum number of shifts
    model.Add(min_shifts_per_nurse <= sum(num_shifts_worked)) 
    #constraints that each nurse must work at most the maximum number of shifts
    model.Add(sum(num_shifts_worked) <= max_shifts_per_nurse)

# pylint: disable=g-complex-comprehension
#tries to maximise the value of the shifts assigned to the nurse who requested them
model.Maximize(
    sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_nurses
        for d in all_days for s in all_shifts))



solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True

'''
solver = cp_model.CpSolver()
status = solver.Solve(model)


if status == cp_model.OPTIMAL:
    print('Solution:')
    for d in all_days:
        print('Day', d)
        for n in all_nurses:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    if shift_requests[n][d][s] == 1:
                        print('Nurse', n, 'works shift', s, '(requested).')
                    else:
                        print('Nurse', n, 'works shift', s,
                              '(not requested).')
        print()
    print(f'Number of shift requests met = {solver.ObjectiveValue()}',
          f'(out of {num_nurses * min_shifts_per_nurse})')
else:
    print('No optimal solution found !')


'''
class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, shifts, num_nurses, num_days, num_shifts, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._shifts = shifts
        self._num_nurses = num_nurses
        self._num_days = num_days
        self._num_shifts = num_shifts
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print('Solution %i' % self._solution_count)
        for d in range(self._num_days):
            print('Day %i' % d)
            for n in range(self._num_nurses):
                is_working = False
                for s in range(self._num_shifts):
                    if self.Value(self._shifts[(n, d, s)]):
                        is_working = True
                        print('  Nurse %i works shift %i' % (n, s))
                if not is_working:
                    print('  Nurse {} does not work'.format(n))
        if self._solution_count >= self._solution_limit:
            print('Stop search after %i solutions' % self._solution_limit)
            self.StopSearch()

    def solution_count(self):
        return self._solution_count

# Display the first five solutions.
solution_limit = 5
solution_printer = NursesPartialSolutionPrinter(shifts, num_nurses,
                                                num_days, num_shifts,
                                                solution_limit)


solver.Solve(model, solution_printer)





