from schedTest import EL
from drs import drs
import random
import math
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from numpy import arange
import TimeDemandAnalysis
import pda
import time

numsets = 1
seed = 0


def main():
    if testtype == 1:       # Ordinary util-based test without TDA
        edf()
    elif testtype == 2:     # Helping method used for period variation test
        edf_cust(100, 100)
    elif testtype == 3:     # Initial approach for period variation test, plotted similarly to util-based test
        edf_dip()
    elif testtype == 4:     # Quantity test used in the thesis. Shows both graphs (Initial and alternative approaches)
        quantity_test()
    elif testtype == 5:     # Exact test used in the thesis. Util-based graph, with TDA and Liu and Layland bound
        tda()
    elif testtype == 6:     # Exact test (constrained-deadline). Includes PDA, sufficient test and plots runtime as well
        const_deadline()
    elif testtype == 7:     # Period variation test used in thesis. Shows total acceptance ratio against parameter 'a'
        multi_dip_test()


# Ordinary utilization-based test without TDA
def edf():
    n = numtasks
    z = 0
    print("Testing EDF-Like Algorithm with implicit deadlines and dynamic priority(EDF). Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatios = []
    utils = []
    while z <= 100:
        utils.append(z)
        numfail = 0
        for x in range(numsets):
            utilization = drs(n, z / 100)
            period = loguniform(n)
            numfail += schedule_tasks(utilization, period, config)
        accRatios.append(1 - (numfail / numsets))
        print("Total utilization:", z, "=> Num of fails: ", numfail, " Acceptance ratio: ", 1 - (numfail / numsets))
        z += utilstep
    plotgraph(accRatios, utils, False)
    exit()


# Helping method for the period variation test. Works only with two tasks and returns the acceptance ratios as an array
def edf_cust(fperiod, speriod):
    z = 0
    accRatios = []
    while z < 100:
        numfail = 0
        for x in range(numsets):
            utilization = drs(numtasks, z / 100)
            period = [fperiod, speriod]
            numfail += schedule_tasks(utilization, period, config)
        accRatios.append(1 - (numfail / numsets))
        z += utilstep
    return accRatios


# Initial approach for exploring period variations
def edf_dip():
    z = 0
    print("Testing EDF-Like Algorithm with implicit deadlines and dynamic priority(EDF). Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep, "| Period step:", periodstep,
          "| Primary period:", primperiod)
    accRatios = []
    utils = []
    while z <= 100:
        utils.append(z)
        failset = [0] * variations
        for x in range(numsets):
            utilization = drs(numtasks, z / 100)
            for i in range(variations):
                period = [primperiod, primperiod + (i * periodstep)]
                failset[i] = failset[i] + schedule_tasks(utilization, period, config)
        for f in range(len(failset)):
            failset[f] = 1 - (failset[f] / numsets)
            failset[f] = round(failset[f], 2)
        accRatios.append(failset)
        print("Total utilization:", z, "=> Num of Acc-Ratio: ", failset)
        z += utilstep
    plotgraph(accRatios, utils, True)
    exit()


# Exact test, uses TDA as an exact test and also shows Liu and Layland bound
def tda():
    n = numtasks
    z = 0
    print("Testing EDF-Like Algorithm with implicit deadlines and fixed-priority(TDA). Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatio_el_dm = []
    accRatio_tda = []
    accRatio_el_edf = []
    utils = []
    while z <= 100:
        utils.append(z)
        numfail_el_dm = 0
        numfail_tda = 0
        numfail_el_edf = 0
        for x in range(numsets):
            utilization = drs(n, z / 100)
            tasks = []
            tdatasks = []
            period = loguniform(n)
            execution = [utilization[i] * period[i] for i in range(len(utilization))]
            sumU = 0
            for y in range(n):
                tasks.append(
                    {'period': period[y], 'execution': execution[y], 'deadline': period[y],
                     'utilization': utilization[y], 'sslength': 0})
                tdatasks.append([period[y], execution[y], period[y]])
                sumU += utilization[y]
            sortedtasks = sorted(tasks, key=lambda item: item['period'])
            tdatasks.sort(key=lambda i: i[0])
            if not EL.EL_fixed(sortedtasks, setprio=2):
                numfail_el_dm += 1
            if not TimeDemandAnalysis.test(tdatasks):
                numfail_tda += 1
            if not EL.EL_fixed(sortedtasks, setprio=3):
                numfail_el_edf += 1
        accRatio_tda.append(1 - (numfail_tda / numsets))
        accRatio_el_dm.append(1 - (numfail_el_dm / numsets))
        accRatio_el_edf.append(1 - (numfail_el_edf / numsets))
        print("Total utilization:", z, "=> Num of fails(EL): ", numfail_el_dm, " Acceptance ratio: ",
              round(1 - (numfail_el_dm / numsets), 1), " Num of fails(TDA): ", numfail_tda,
              " Acceptance ratio: ", 1 - (numfail_tda / numsets))
        z += utilstep

    plotgraph([accRatio_el_dm, accRatio_tda, accRatio_el_edf], utils, False)
    exit()


# Quantity test used in thesis
def quantity_test():
    z = 0
    print("Testing EDF-Like Algorithm with implicit deadlines and dynamic priority(EDF). Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatios = []
    utils = []
    totalaccratio = [0] * variations
    taskamount = []
    for j in range(variations):
        taskamount.append(numtasks + (j * numtaskstep))

    while z <= 100:
        utils.append(z)
        failset = [0] * variations
        for i in range(variations):
            numfail = 0
            n = taskamount[i]
            for x in range(numsets):
                utilization = drs(n, z / 100)
                period = loguniform(n)
                numfail += schedule_tasks(utilization, period, config)
            failset[i] = round(1 - (numfail / numsets), 2)
            totalaccratio[i] += failset[i]
        accRatios.append(failset)
        print("Total utilization:", z, "=> Acceptance ratio: ", failset)
        z += utilstep

    for i in range(len(totalaccratio)):
        totalaccratio[i] = round(totalaccratio[i] / ((100 / utilstep) + 1), 3)

    print(totalaccratio)
    plotgraph([accRatios, totalaccratio], [utils, taskamount], True)
    exit()


# Exact test for constrained-deadline task sets. Uses PDA as an exact test and a sufficient test. Shows runtime as well
def const_deadline():
    z = 0
    print("Testing EDF-Like Algorithm with constraint deadlines and dynamic priority(EDF). Number of task sets:",
          numsets, "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatio_el_edf = []
    accRatio_el_dm = []
    accRatio_pda = []
    accRatio_suf = []
    accRatio_tda = []
    utils = []
    period = []
    runtime_arr = []

    for j in range(numtasks):
        period.append(pow(2, j + 1))
    while z <= 100:
        utils.append(z)
        numfail_pda = 0
        numfail_suf = 0
        numfail_el_edf = 0
        numfail_el_dm = 0
        numfail_tda = 0

        runtime_el_edf = runtime_el_dm = runtime_pda = runtime_suf = 0

        for x in range(numsets):
            if z == 0:
                utilization = drs(numtasks, 0.01 / 100)
            else:
                utilization = drs(numtasks, z / 100)
            deadline = [i * ppercentage for i in period]

            start = time.time()
            numfail_el_edf += schedule_tasks(utilization, period, 3, deadline)
            end = time.time()
            runtime_el_edf += end - start

            start = time.time()
            numfail_el_dm += schedule_tasks(utilization, period, 2, deadline)
            end = time.time()
            runtime_el_dm += end - start

            execution = [utilization[i] * period[i] for i in range(len(utilization))]
            pdatasks = []

            for m in range(len(utilization)):
                pdatasks.append([period[m], execution[m], deadline[m], utilization[m]])

            start = time.time()
            if not pda.pda(pdatasks):
                numfail_pda += 1
            end = time.time()
            runtime_pda += end - start

            start = time.time()
            if not cd_suff_test(pdatasks):
                numfail_suf += 1
            end = time.time()
            runtime_suf += end - start

            if not TimeDemandAnalysis.test(pdatasks):
                numfail_tda += 1

        accRatio_el_edf.append(1 - (numfail_el_edf / numsets))
        accRatio_el_dm.append(1 - (numfail_el_dm / numsets))
        accRatio_pda.append(1 - (numfail_pda / numsets))
        accRatio_suf.append(1 - (numfail_suf / numsets))
        accRatio_tda.append(1 - (numfail_tda / numsets))
        print("Total utilization:", z, "=> Num of fails: (EL-edf)", numfail_el_edf, "(EL-dm)", numfail_el_dm, "(PDA)",
              numfail_pda, "(Sufficient Test)", numfail_suf, "; Acceptance ratio: (EL-edf)",
              round((1 - (numfail_el_edf / numsets)), 2), "(EL-dm)", round((1 - (numfail_el_dm / numsets)), 2), "(PDA)",
              round((1 - (numfail_pda / numsets)), 2), "(Sufficient Test)", round((1 - (numfail_suf / numsets)), 2))
        print("Total utilization:", z, "=> Runtime: (EL-edf)", runtime_el_edf, "(EL-dm)", runtime_el_dm, "(PDA)",
              runtime_pda, "(Sufficient Test)", runtime_suf)
        runtime_arr.append([runtime_el_edf, runtime_el_dm, runtime_pda, runtime_suf])
        z += utilstep
    plotgraph([accRatio_el_edf, accRatio_el_dm, accRatio_pda, accRatio_suf, accRatio_tda], utils, False)
    #plotruntime(runtime_arr, utils)                        # Uncomment if runtime is needed
    exit()


# Sufficient test for constrained-deadline task sets
def cd_suff_test(tasks):
    tasks.sort(key=lambda n: n[2])  # Sort task set by deadline
    for k in range(len(tasks)):
        sum_U = 0
        sum_G = 0
        for i in range(k + 1):
            task = tasks[i]
            sum_U += task[3]
            sum_G += (task[1] * (task[0] - task[2])) / task[0]
        result = sum_U + ((1 / tasks[k][2]) * sum_G)
        if result > 1:
            return False
    return True


# Period variation test used in thesis
def multi_dip_test():
    m = 1
    totalaccratio = []
    a_points = []
    a_step = periodstep / primperiod
    print("Testing multi-dip of EDF-Like with implicit deadline and dynamic priority(EDF)\nParameter 'a' step:", a_step,
          "| Primary period for T_1:", primperiod, "| Number of task sets per 'a' parameter point:", numsets,
          "| Number of tasks per task set:", numtasks, "| Utilization step:", utilstep)
    while m <= aparam:
        result = edf_cust(primperiod, primperiod * m)
        result = round(sum(result), 2)
        totalaccratio.append(round(result / (100 / utilstep), 3))
        a_points.append(m)
        print("Parameter 'a' in T_2 = a * T_1:", m, "=> Total overall Acceptance ratio for the given 'a':",
              round(result / (100 / utilstep), 3))
        m = round(m + a_step, 3)
    print(totalaccratio)
    print(a_points)
    plotgraph(totalaccratio, a_points, False)


# Helping method for running EDF-Like schedulability test on a given task set
def schedule_tasks(utilization, period, prio, deadline=None):
    if deadline is None:
        deadline = period
    tasks = []
    execution = [utilization[i] * period[i] for i in range(len(utilization))]
    for y in range(len(utilization)):
        tasks.append(
            {'period': period[y], 'execution': execution[y], 'deadline': deadline[y],
             'utilization': utilization[y], 'sslength': 0})
    sortedtasks = sorted(tasks, key=lambda item: item['period'])
    if not EL.EL_fixed(sortedtasks, setprio=prio):
        return 1
    else:
        return 0


# Plots runtime of constrained-deadline test
def plotruntime(runtime, u):
    names = ["EL-EDF", "EL-DM", "PDA", "Sufficient Test"]
    for x in range(4):
        arr = []
        for i in range(len(runtime)):
            arr.append(runtime[i][x])
        plt.plot(u, arr, label=names[x])
        plt.scatter(u, arr)
    plt.xlabel('Utilization (%)')
    plt.ylabel('Runtime in seconds')
    plt.title(str(numsets) + " Task Sets with " + str(numtasks) + " Tasks each")
    plt.legend(loc="best")
    # plt.yticks(arange(0.8, step=0.10))
    plt.show()


# PLots all the data depending on the test type chosen
def plotgraph(a, u, mul):
    plt.rcParams["font.family"] = ["sans-serif"]
    plt.rcParams["font.size"] = 14
    plt.rcParams["figure.figsize"] = (7, 5)

    if mul:
        if testtype == 4:
            accratios = a[0]
            utils = u[0]
            totalaccratios = a[1]
            taskamount = u[1]
            for x in range(variations):
                arr = []
                for i in range(len(accratios)):
                    arr.append(accratios[i][x])
                plt.plot(utils, arr, label=str(numtasks + (x * numtaskstep)))
                plt.scatter(utils, arr)
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.legend(loc="lower left")
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
            plt.show()

            plt.plot(taskamount, totalaccratios)
            plt.scatter(taskamount, totalaccratios)
            plt.xlabel('Number of Tasks per Set')
            plt.ylabel('Total Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(numtasks, numtasks + (variations * numtaskstep), step=numtaskstep))

        else:
            for x in range(variations):
                arr = []
                for i in range(len(a)):
                    arr.append(a[i][x])
                plt.plot(u, arr,
                         label=str(primperiod + (x * periodstep)) + " (" + str(
                             round((x * periodstep * 100) / primperiod)) + "%)")
                plt.scatter(u, arr)
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.legend(loc="lower left")
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
    else:
        if testtype == 5:
            plt.plot(u, a[1], label="TDA")
            plt.scatter(u, a[1])
            plt.plot(u, a[0], label="EL-DM")
            plt.scatter(u, a[0])
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
            plt.fill_between(u, a[0], a[1], color='grey', alpha=0.5)
            plt.plot(u, a[2], label="EL-EDF")
            plt.scatter(u, a[2])
            if numtasks >= 10:
                plt.axvline(x=69.3147, label="L&L Bound", color='r')
            else:
                bound = numtasks * (pow(2, 1 / numtasks) - 1)
                plt.axvline(x=bound * 100, label="L&L Bound", color='r')
            plt.legend(loc="lower left")
        elif testtype == 6:
            names = ["EL-EDF", "EL-DM", "PDA", "Sufficient Test", "TDA"]
            for i in range(5):
                plt.plot(u, a[i], label=names[i])
                plt.scatter(u, a[i])
            plt.title("Constraint Deadline with " + str(ppercentage * 100) + "%")
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
            plt.legend(loc="lower left")
        elif testtype == 7:
            plt.plot(u, a, zorder=0)
            plt.scatter(u, a)
            plt.xlabel('Parameter \'a\'')
            plt.ylabel('Total Acceptance Ratio')
            if aparam == 3:
                min_tar = 1
                min_a_point = 0
                for i in range(len(a)):
                    if a[i] < min_tar:
                        min_tar = a[i]
                        min_a_point = u[i]
                min_y = min(a)
                plt.xticks(arange(1, 3.01, 0.1))
                min_y = (math.floor(min_y * 100) - 1) / 100
                plt.yticks(arange(min_y, 1.01, 0.01))
                plt.scatter(min_a_point, min_tar, color='red', zorder=1)
            else:
                # For EDF arange(0.84, 1.01, step=0.02)), for DM arange(0.92, 1.01, step=0.02))
                plt.yticks(arange(0.92, 1.01, step=0.02))
                # For EDF arange(1, aparam+0.1, step=1), for DM arange(arange(1, aparam+0.1, step=0.5))
                plt.xticks(arange(1, aparam + 0.1, step=0.5))
        else:
            plt.plot(u, a)
            plt.scatter(u, a)
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))

    plt.show()


# Log-uniform distribution used to generate periods of a task set
def loguniform(n, Tmin=1, Tmax=100, base=10) -> list[float]:
    TSet = []
    for i in range(n):
        TSet.append(
            math.pow(base, random.uniform(math.log(Tmin, base), math.log(Tmax, base)))
        )
    return TSet


if __name__ == "__main__":
    # Different options are available for the test
    parser = ArgumentParser()
    parser.add_argument("-tt", "--testtype", dest="ttype", type=int, default=1,
                        help="Choose the type of test to be used.")
    parser.add_argument("-ts", "--tasksets", dest="tsets", type=int, default=1, help="Specify the number of task sets.")
    parser.add_argument("-nt", "--numoftasks", dest="ntasks", type=int, default=10,
                        help="Specify the number of tasks in a task set.")
    parser.add_argument("-us", "--utilstep", dest="ustep", type=float, default=10, help="Specify the utilization step.")
    parser.add_argument("-pp", "--primaryperiod", dest="pperiod", type=int, default=1,
                        help="Specify the primary period to be used for the edf dip analysis")
    parser.add_argument("-ps", "--periodstep", dest="pstep", type=float, default=0,
                        help="Specify the period step for the dip analysis")
    parser.add_argument("-v", "--variations", dest="var", type=int, default=2,
                        help="Specify the amount of plots to be created.")
    parser.add_argument("-nts", "--numtaskstep", dest="ntstep", type=int, default=0,
                        help="Specify the amount of change for the number of tasks per task set.")
    parser.add_argument("-cd", "--constdead", dest="cdead", type=float, default=0.9,
                        help="Specify the percentage of the periods to be used for constraint deadlines.")
    parser.add_argument("-a", "--aparam", dest="a", type=int, default=2,
                        help="Specify the 'a' parameter for the multi-dip test.")
    parser.add_argument("-co", "--config", dest="config", type=int, default=3,
                        help="Specifies which configuration EDF-Like should use, 2 for EL-DM and 3 for EL-EDF")
    parser.add_argument("-s", "--seed", dest="seed", type=int, default=200, help="Specify seed for random generation.")
    args = vars(parser.parse_args())

    testtype = args["ttype"]
    numsets = args["tsets"]
    numtasks = args["ntasks"]
    utilstep = args["ustep"]
    primperiod = args["pperiod"]
    periodstep = args["pstep"]
    variations = args["var"]
    numtaskstep = args["ntstep"]
    ppercentage = args["cdead"]
    aparam = args["a"]
    config = args["config"]
    seed = args["seed"]

    random.seed(seed)

    if testtype == 3 or testtype == 7:
        numtasks = 2

    # Example of executing ordinary util-based test in terminal:
    # python3 EL_testing.py -tt 1 -ts 20 -nt 5 -us 10 -co 3 -s 1

    # For edf-dip, number of tasks should always be equal to 2
    # Like so: python3 EL_testing.py -tt 3 -ts 10 -nt 2 -us 5 -pp 100 -ps 80 -v 10 -co 2-s 1

    # For exact test with TDA:
    # Like so: python3 EL_testing.py -tt 5 -ts 10 -nt 10 -us 5 -s 5

    # For quantity of tasks per task set test:
    # python3 EL_testing.py -tt 4 -ts 20 -nt 5 -us 5 -v 3 -nts 10 -co 2 -s 2

    # For period variation test(Number of tasks = 2):
    # python3 EL_testing.py -tt 7 -ts 100 -nt 2 -us 5 -pp 100 -ps 20 -a 5 -co 2 -s 2

    # For constrained-deadline test with PDA:
    # python3 EL_testing.py -tt 6 -ts 100 -nt 10 -us 5 -cd 0.6 -s 2

    main()
