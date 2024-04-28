from schedTest import EL
from drs import drs
import random
import math
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from numpy import arange
import TimeDemandAnalysis

numsets = 1
seed = 0


def main():
    if testtype == 1:
        edf()
    elif testtype == 2:
        edf_cust()
    elif testtype == 3:
        edf_dip()
    elif testtype == 4:
        tda()


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
            utilization = drs(n, z/100)
            period = loguniform(n)
            numfail += schedule_tasks(utilization, period, 3)
        accRatios.append(1 - (numfail / numsets))
        print("Total utilization:", z, "=> Num of fails: ", numfail, " Acceptance ratio: ", 1 - (numfail / numsets))
        z += utilstep
    plotgraph(accRatios, utils, False)
    exit()


def edf_cust():
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
            # utilization.sort()
            period = loguniform(n)
            period.sort()
            # period[n-3] = 220
            # period[n-2] = 221
            # period[n-1] = 222
            numfail += schedule_tasks(utilization, period, 3)
        accRatios.append(1 - (numfail / numsets))
        z += utilstep
        print("Total utilization:", z, "=> Num of fails: ", numfail, " Acceptance ratio: ", 1 - (numfail / numsets))
    plotgraph(accRatios, utils, False)
    exit()


def edf_dip():
    z = 0
    print("Testing EDF-Like Algorithm with implicit deadlines and dynamic priority(EDF). Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep, "| Period step:", periodstep)
    accRatios = []
    utils = []
    while z <= 100:
        utils.append(z)
        failset = [0, 0, 0, 0, 0, 0]
        for x in range(numsets):
            utilization = drs(numtasks, z/100)
            # utilization.sort()
            for i in range(6):
                period = [100, 100 + (i*periodstep)]
                failset[i] = failset[i] + schedule_tasks(utilization, period, 3)
        for f in range(len(failset)):
            failset[f] = 1 - (failset[f] / numsets)
            failset[f] = round(failset[f], 2)
        accRatios.append(failset)
        print("Total utilization:", z, "=> Num of Acc-Ratio: ", failset)
        z += utilstep
    plotgraph(accRatios, utils, True)
    exit()


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
            utilization = drs(n, z/100)
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
            if both:
                if not EL.EL_fixed(sortedtasks, setprio=3):
                    numfail_el_edf += 1
        accRatio_tda.append(1 - (numfail_tda / numsets))
        accRatio_el_dm.append(1 - (numfail_el_dm / numsets))
        accRatio_el_edf.append(1 - (numfail_el_edf / numsets))
        print("Total utilization:", z, "=> Num of fails(EL): ", numfail_el_dm, " Acceptance ratio: ",
              round(1 - (numfail_el_dm / numsets), 1), " Num of fails(TDA): ", numfail_tda, 1-(numfail_tda / numsets))
        z += utilstep

    plotgraph([accRatio_el_dm, accRatio_tda, accRatio_el_edf], utils, False)
    exit()


def schedule_tasks(utilization, period, prio):
    tasks = []
    execution = [utilization[i] * period[i] for i in range(len(utilization))]
    sumU = 0
    for y in range(numtasks):
        tasks.append(
            {'period': period[y], 'execution': execution[y], 'deadline': period[y],
             'utilization': utilization[y], 'sslength': 0})
        sumU += utilization[y]
    sortedtasks = sorted(tasks, key=lambda item: item['period'])
    # for x in sortedtasks:
    #     print("Period:", x['period'], "Execution:", x['execution'])
    if not EL.EL_fixed(sortedtasks, setprio=prio):
        return 1
    else:
        return 0


def plotgraph(a, u, mul):
    if mul:
        markers = ["o", ",", "v", "^", "<", ">"]
        for x in range(6):
            arr = []
            for i in range(len(a)):
                arr.append(a[i][x])
            plt.plot(u, arr, label=str(100 + x*periodstep) + " (" + str((x*periodstep*100)/100) + "%)")
            plt.scatter(u, arr, marker=markers[x])
        plt.xlabel('Utilization (%)')
        plt.ylabel('Acceptance Ratio')
        plt.legend(loc="lower left")
        plt.yticks(arange(1.1, step=0.10))
        plt.xticks(arange(101, step=10))
        plt.show()
    else:
        if len(a) > 1:
            plt.plot(u, a[0])
            plt.scatter(u, a[0])
            plt.plot(u, a[1])
            plt.scatter(u, a[1])
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
            plt.fill_between(u, a[0], a[1], color='grey', alpha=0.5)
            if numtasks >= 10:
                plt.axvline(x=69.3147, color='r')
            else:
                bound = numtasks * (pow(2, 1/numtasks) - 1)
                plt.axvline(x=bound*100, color='r')
            if both:
                plt.plot(u, a[2])
                plt.scatter(u, a[2])
            plt.show()
        else:
            plt.plot(u, a)
            plt.scatter(u, a)
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
            plt.show()


def loguniform(n, Tmin=1, Tmax=100, base=10) -> list[float]:
    TSet = []
    for i in range(n):
        TSet.append(
            math.pow(base, random.uniform(math.log(Tmin, base), math.log(Tmax, base)))
        )
    return TSet


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-tt", "--testtype", dest="ttype", type=int, default=1,
                        help="Choose the type of test to be used.")
    parser.add_argument("-ts", "--tasksets", dest="tsets", type=int, default=1, help="Specify the number of task sets.")
    parser.add_argument("-nt", "--numoftasks", dest="ntasks", type=int, default=10,
                        help="Specify the number of tasks in a task set.")
    parser.add_argument("-us", "--utilstep", dest="ustep", type=float, default=10, help="Specify the utilization step.")
    parser.add_argument("-ps", "--periodstep", dest="pstep", type=int, default=0,
                        help="Specify the period step for the dip analysis")
    parser.add_argument("-b", "--both", dest="both", type=int, default=False, help="Show both tests.")
    parser.add_argument("-s", "--seed", dest="seed", type=int, default=200, help="Specify seed for random generation.")
    args = vars(parser.parse_args())

    testtype = args["ttype"]
    numsets = args["tsets"]
    numtasks = args["ntasks"]
    utilstep = args["ustep"]
    periodstep = args["pstep"]
    both = args["both"]
    seed = args["seed"]

    random.seed(seed)

    # Example of execution in terminal:
    # python3 EL_testing.py -tt 1 -ts 20 -nt 5 -us 10

    # For edf-dip, number of tasks should always be equal to 2
    # Also the period step should be given: python3 EL_testing.py -tt 3 -ts 10 -nt 2 -us 5 -ps 80 -s 1

    # For TDA test the el algorithm with dynamic priority can also be included into the graph by using the arg --both
    # Like so: python3 EL_testing.py -tt 4 -ts 10 -nt 10 -us 5 -b 1 -s 5

    main()
