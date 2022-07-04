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


T_final = len(targetdataValue) # final time incriment
num_sats = 65    # illuminating satellites
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
    



# adding storage constraints
Data_per_Obs = 25000
Down_link_rate = 250000


for t in all_T:
    delta_pos_data =sum( Data_per_Obs * targetIlum[t][s]   for s in all_sats) 
    delta_neg_data = sum(Down_link_rate * Downlink[t])
    
sum(targetIlum[1][s] * targetdataValue[1][s] for s in all_sats)
'''
Maxstorage = 1e9
for tau in all_T:
   model.Add(sum(Data_per_Obs * targetIlum[t][s] *action[t][s] - Down_link_rate * Downlink[t] * action[t][66]     for s in all_sats for t in range(0,tau) ) < Maxstorage)
        


'''












