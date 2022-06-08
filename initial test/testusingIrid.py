# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 09:25:29 2022


Test code for trying to use google OR tools with some Strathcube data

@author: iainh
"""


# code to import the potential target data
import pandas as pd
import numpy as np
from ortools.sat.python import cp_model

model = cp_model.CpModel()

data = pd.read_csv("Iridium view data log.csv")

targetdata = data.values.tolist()


#finding the maximum possible amount of observation
total = 0
for i in range(0,len(targetdata)):
    for j in range(0,len(targetdata[i])):
        total = total+targetdata[i][j]

print(total)

all_timeincrements = range(i+1)
all_targets = range(j+1)


# creates boolean array containing which satellite is being targeted and adds
# the constraint that only one satellite may be targeted at a time

targets = {}
for ti in all_timeincrements:
    for tr in all_targets:
        targets[(ti,tr)] = model.NewBoolVar('shift_time%itarget%i' % (ti,tr))

for ti in all_timeincrements:
    model.AddAtMostOne(targets[(ti,tr)] for tr in all_targets)
  
#creating a power and energy variables
energy = model.NewIntVar(0,24000,'Energystored')

# note the power variable doesn't represent a power demand but a change in stored
# energy for a given time increment
power = {} 
for ti in all_timeincrements:
    power[(ti)] = model.NewIntVar(-25,25,'ChangeinStoredenergy')


model.add(sum(power[(ti)]) for ti in all_timeincrements > 0)


# adds objective to maximise the amount of targeted satellites that are also in 
# view, i.e. to maximise the time the PBR can potentially operate
model.Maximize(sum(targetdata[ti][tr]* targets[(ti,tr)]  for tr in all_targets for ti in all_timeincrements))


# Creates the solver and solve.
solver = cp_model.CpSolver()
status = solver.Solve(model)

operating_time = 0

for ti in all_timeincrements:
    for tr in all_targets:
        operating_time = operating_time + solver.Value(targets[(ti,tr)])



if status == cp_model.OPTIMAL:
    print('Solution:')
   # print( f'Time increments spent in operational pointing = {solver.ObjectiveValue()}', 'out of %i' %(total)  ) 
    
    print('total time spent targeting a satellite = %i' % (operating_time))
    
          
print("executed without error")






