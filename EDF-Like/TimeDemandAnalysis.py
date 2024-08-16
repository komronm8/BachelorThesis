import numpy as np
import math


# The tasks is an Array with three columns and n Rows
# Each Row represents one Task
# The columns hold the Tasks parameters
# column 0 is period P,
# column 1 is WCET C
# column 2 is deadline D
# P_i is accessed as: tasks[i][0]
# C_i is accessed as: tasks[i][1]
# D_i is accessed as: tasks[i][2]

# Workload function for task i in ordered tasks
# Will return the Workload or -1 if not feasible


# Function to determine if task i can meet its deadline based on workload analysis
def workload(tasks, i):
    t = 0
    for x in range(i):
        t += tasks[x][1]
    # print(tasks[i][2])
    # print(t)
    while t <= tasks[i][2]:
        wl = calculate_workload(tasks, i, t)
        if wl <= t:
            # print("true")
            return True
        t = wl
    return False


# Function to calculate the workload for task i at a given time t
def calculate_workload(tasks, i, t):
    C_i = tasks[i][1]
    sum = 0
    for k in range(i):
        C_k = tasks[k][1]
        T_k = tasks[k][0]
        sum = sum + (math.ceil(t / T_k) * C_k)
    return C_i + sum


# Function to perform TDA on a list of tasks
def test(tasks):

    for x in range(len(tasks)):
        if not workload(tasks, x):
            return False

    return True
