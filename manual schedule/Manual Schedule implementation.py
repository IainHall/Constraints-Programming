# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 11:39:55 2022

@author: iainh

Script used to create an offline schedule using a manual heuristic for STRATHcube

non optimal and will prioritise tasks based on only information at a single point in time
will prioritise:
    Downlinking    
    Observing
    Processing
    Idle
these actions are held in an action array where 
0 = observing
1 = downlink
2 = Processing
3 = idle
"""


# code to import the potential target data
import pandas as pd
import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt


#read in the illuminator data value (avg objects detected in time increment)
data = pd.read_csv("Avg objects Detection log.csv")
target_value = data.values.tolist()

data = pd.read_csv("illuminator available.csv")
ilum_in_view = data.values.tolist()

#read in the downlink data times
data = pd.read_csv("Communications Data Log.csv")
downlink_possible= data.values.tolist() 

num_T = len(target_value) # final time incriment
num_sats = 66   # illuminating satellites
num_actions = 4
all_sats = range(num_sats)   
all_T = range(num_T)
all_actions = range(num_actions)

action = [0 for a in all_actions for t in all_T] #4 by time length variable
target_sat = [0 for s in all_sats for t in all_T]

#constrained resource variables
# note memory is in kB
maxStorage = 64e3
dataPerObs = 1500

storedData= 0
ObsStored = 0
Processed = 0 
Downlinks = 0
ObservedValue = {}
ObsValIndex = 0
ProcessedValue = {}
ProValIndex = 0
DownlinkedValue = {}
DownValIndex = 0

# Heuristic implementation within loop
for t in all_T:
    
    if downlink_possible[t] == 1 and Processed > 1: # downlink decision
        
        DownlinkedValue.append(ProcessedValue[ProValIndex])
            
        action[2][t] = 1
        storedData = storedData - 250
        Downlinks += 1
        
    elif ilum_in_view[t] == 1 and storedData <= maxStorage + dataPerObs:  # observe decision
    
        ObservedValue.append(max(target_value[s][t] for s in all_sats))
        storedData = storedData + dataPerObs
        ObsStored += 1
        
    elif ObsStored > 1:      # process decision
    
        ProcessedValue.append(ObservedValue[ObsValIndex])
        ObsValIndex += 1
        
        ObsStored -= 1 
        Processed += 1
        storedData = storedData - dataPerObs 
        
    else:
        action[3][t] =1     # idle decision
        










