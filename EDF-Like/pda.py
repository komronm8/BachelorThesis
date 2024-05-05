from math import floor, lcm


# Task tau_i contribution to demand bound function
def dbf_contribution(task, t):
    return floor((t + task[0] - task[2]) / task[0]) * task[1]


# Total value of demand bound function
def dbf(tasks, t):
    dbf_total = 0
    for task in tasks:
        dbf_total += dbf_contribution(task, t)
    return dbf_total


# Test demand bound function over test set
def pda(tasks):
    L = 0
    U = 0
    H = 1
    D_max = 0
    for task in tasks:
        U_i = task[1] / task[0]             # Utilization of tau_i
        U += U_i                            # Total utilization
        L += (task[0] - task[2]) / U_i
        H = lcm(H, task[0])                 # Hyperperiod
        D_max = max(D_max, task[2])

    if U < 1:
        L /= (1 - U)
        D_max = min(H, max(D_max, L))
    else:
        for task in tasks:
            if task[2] < task[0]:
                return False
        return U == 1

    if D_max < 0:
        print(f"Problem with D_max={D_max}!")

    for task in tasks:
        deadline = task[2]
        while deadline <= D_max:
            if dbf(tasks, deadline) > deadline:
                return False
            deadline += task[0]

    return True
