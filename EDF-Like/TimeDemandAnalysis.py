import numpy as np
import math


# The tasks is an Array with three columns and n Rows
# Each Row represents one Task
# The columns hold the Tasks parameters
# column 0 is period P,
# column 1 is deadline D
# column 2 is WCET C
# P_i is accessed as: tasks[i][0]
# D_i is accessed as: tasks[i][1]
# C_i is accessed as: tasks[i][2]
# The number of tasks can be accessed as: tasks.shape[0]

# Workload function for task i in ordered tasks
# Will return the Workload or -1 of not feasible


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


def calculate_workload(tasks, i, t):
    C_i = tasks[i][1]
    sum = 0
    for k in range(i):
        C_k = tasks[k][1]
        D_k = tasks[k][2]
        sum = sum + (math.ceil(t / D_k) * C_k)
    return C_i + sum


# The Time Demand Analysis Test
def test(tasks):
    # Sorting Taskset by Period/Deadline
    # This makes implementing TDA a lot easier
    # shape = tasks.shape
    # sortedtasks = tasks[tasks[:, 0].argsort()]

    for x in range(len(tasks)):
        if not workload(tasks, x):
            return False

    return True
