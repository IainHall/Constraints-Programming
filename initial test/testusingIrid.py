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

#read in the iridium view time data
data = pd.read_csv("Iridium view data log.csv")
targetdata = data.values.tolist()

#read in the eclipse time data
data = pd.read_csv("Eclipse data log.csv")
eclipseData = data.values.tolist()

#finding the maximum possible amount of observation
total = 0
for i in range(0,len(targetdata)):
    for j in range(0,len(targetdata[i])):
        total = total+targetdata[i][j]

print(total)

all_timeincrements = range(i+1)
all_targets = range(j+1)


powerCost = [-2, -4, -40]
all_operations = range(len(powerCost))


# creates boolean array containing which satellite is being targeted and adds
# the constraint that only one satellite may be targeted at a time

#light =  {}
#for ti in all_timeincrements:
#    light[ti] = model.NewBoolVar('In sun at time index %i' % (ti))


targets = {}
for ti in all_timeincrements:
    for tr in all_targets:
        targets[(ti,tr)] = model.NewBoolVar('shift_time%itarget%i' % (ti,tr))

for ti in all_timeincrements:
    model.AddAtMostOne(targets[(ti,tr)] for tr in all_targets)
    

powerop = {}
for ti in all_timeincrements:
    for op in all_operations:
       powerop= model.NewBoolVar('power op: time %i op %i' % (ti,op))
'''
#creating a power and energy variables
energy = {}
for ti in all_timeincrements:
    energy[ti] = model.NewIntVar(0,24000,'Energystored at time %i ' % (ti))

# note the power variable doesn't represent a power demand but a change in stored
# energy for a given time increment
power = {} 
for ti in all_timeincrements:
        power[(ti)] = model.NewIntVar(-25,25,'ChangeinStoredenergy time%i' % (ti))


for ti in all_timeincrements:
    model.Add(power[ti] == )
#model.Add(powerop[(1,0)] == 1).OnlyEnforceIf(sum(targets[(1,tr)] for tr in all_targets) > 0)
#   model.Add(powerop[(ti,1)]==1).OnlyEnforceIf()
#for ti in all_timeincrements:
#    model.AddImplication(sum(targets[(ti,tr)] for tr in all_targets) > 0, energy[ti] = -2)    
'''
temp = {}
    
for ti in all_timeincrements: 
    for op in all_operations:
        temp[ti] = temp[ti] + powerCost[op]*powerop[ti,op]
    
    
model.Add(sum(sum(powerCost[op]* powerop[ti,op]) for op in all_operations) for ti in all_timeincrements > 0)
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






