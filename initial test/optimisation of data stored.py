# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:33:42 2022

@author: iainh



Optimisation of data stored for SC

"""

# code to import the potential target data
import pandas as pd
import numpy as np
from ortools.sat.python import cp_model

model = cp_model.CpModel()

#read in the illuminator data value (avg objects detected in time increment)
data = pd.read_csv("Avg objects Detection log.csv")
targetdataValue = data.values.tolist()

#read in valid illuminators to target
data = pd.read_csv("Illuminator view data log.csv")
targetIlum = data.values.tolist()

#read in the downlink data times
data = pd.read_csv("Communications Data Log.csv")
Downlink = data.values.tolist()
Downlinknp = np.array(Downlink)

#read in the memory demands
data = pd.read_csv("Demands.csv")
demand  = data.values.tolist()


T_final = len(targetdataValue) # final time incriment
num_sats = 66   # illuminating satellites
num_actions = num_sats+1


all_sats = range(num_sats)   
all_T = range(T_final)
all_actions = range(num_actions)

# creates a boolean vector for what action the satellite can take when
action = {}
for t in all_T:
    for a in all_actions:
        action[(t, a)] = model.NewBoolVar('action_t%ia%i' % (t, a))

# create a rule that only one action can occur at any time incriment t
for t in all_T:
    model.AddAtMostOne(action[(t,a)] for a in all_actions)

storedData = {}
for t in all_T:
    storedData =  model.NewIntVar(0,10000,'stored_data_t%i' % t)

#for t in range(2,T_final):
 #   model.Add(storedData[(t)] == storedData[(t-1)])

isAction = {}
for t in all_T:
    isAction = model.NewBoolVar('Action at t = %i' % t)



# adding storage constraints
Data_per_Obs = 25   #kB
Down_link_rate = 250
Maxstorage = 10000

times = []
for t in all_T:
    times.append(t)
#for t in all_T:
 #   model.AddReservoirConstraintWithActive(times[t], demand,sum(action[(t,a)] for a in all_actions)  ,0, Maxstorage)

maxDownlinkarray = sum(Down_link_rate * Downlinknp[t]  for t in all_T )   
maxDownlink = maxDownlinkarray[0]
model.Add(sum(Data_per_Obs*action[(t,a)] * targetIlum[t][a]   for a in all_sats for t in all_T)  <  maxDownlink )


# making objective function
model.Maximize(sum(action[(t,a)] * targetdataValue[t][a] for a in all_sats for t in all_T))

totalvalue = 0
for t in all_T:
    totalvalue = totalvalue+ max(targetdataValue[t])
print(totalvalue)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print('Optimal solution found')
    print(f'total value stored = {solver.ObjectiveValue()}' )
    
    
    out =[ [solver.Value(action[(t,a)]) for a in all_actions] for t in all_T ]
    
    outdata = pd.DataFrame(out)
    outdata.to_csv('Chosen Actions.csv')
    

    
    
    
    
else:
    print('no optimal solution found')
            
'''
t = 1
model.AddReservoirConstraint(t,sum( Data_per_Obs*action[(t,a)] * targetIlum[t][a] for a in all_sats ),0, Maxstorage)


for tau  in all_T:
    trange = range(tau) 
    model.Add( sum( Data_per_Obs*action[(t,a)] * targetIlum[t][a] for a in all_sats for t in trange )    < Maxstorage )
    print(tau)
             # - sum(Down_link_rate* action[(t,num_actions-1)] * Downlink[t] for t in trange)        \
           


        #  delta_pos_data =sum( Data_per_Obs * targetIlum[t][s]   for s in all_sats) 
        #delta_neg_data = sum(Down_link_rate * Downlink[t])
'''

print('executed')
'''

Maxstorage = 1e9
for tau in all_T:
   model.Add(sum(Data_per_Obs * targetIlum[t][s] *action[t][s] - Down_link_rate * Downlink[t] * action[t][66]     for s in all_sats for t in range(0,tau) ) < Maxstorage)
        


'''












