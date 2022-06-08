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

all_timeincrements = range(i)
all_targets = range(j)

targets = {}
for ti in all_timeincrements:
    for tr in all_targets:
        targets[(ti,tr)] = model.NewBoolVar('shift_time%itarget%i' % (ti,tr))








