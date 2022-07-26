# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 14:57:19 2022

@author: iainh


Using Job shop method to control the scheduling of satellite operations

"""


# code to import the potential target data
import collections
import pandas as pd
import numpy as np
import matplotlib as mlp
import matplotlib.pyplot as plt
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

T_final = 2000;#len(targetdataValue)
num_sats = 66#  len(targetdataValue[0])
all_T = range(T_final)
all_sat = range(num_sats)


downlinktime = 1
observetime  = 4
processtime = 20
taskduration = [observetime , processtime, downlinktime]
maximum = T_final*66* sum(taskduration)

jobset= [ taskduration for s in all_sat]
job = [jobset for t in all_T]
 
task_type = collections.namedtuple('task_type', 'start end interval')
intervals = collections.defaultdict(list)

all_tasks = {}       
        
for t in all_T:
    for s in all_sat:   
        for task_id, task  in enumerate(job[t][s]):
            suffix = '_t%i_s%i_task%i' % (t, s, task_id)
            start_var = model.NewIntVar(0, maximum, 'start' + suffix)
            end_var = model.NewIntVar(0, maximum, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, task, end_var, 'Interval' + suffix )
            all_tasks[t, s, task_id] = task_type(start=start_var, end=end_var,interval=interval_var)
            intervals[0].append(interval_var)

model.AddNoOverlap(intervals)

for t, jobset in enumerate(job):
    for s, task in enumerate(jobset):
        for task_id in range(len(task-1)):
            model.Add(all_tasks[t,s,task_id+1].start >= all_tasks[t,s,task_id].end)


