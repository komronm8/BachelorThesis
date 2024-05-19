from schedTest import EL
from drs import drs
import random
import math
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from numpy import arange
import TimeDemandAnalysis
import pda

numsets = 1
seed = 0


def main():
    if testtype == 1:
        edf()
    elif testtype == 2:
        edf_cust(100, 100)
    elif testtype == 3:
        edf_dip()
    elif testtype == 4:
        quantity_test()
    elif testtype == 5:
        tda()
    elif testtype == 6:
        const_deadline()
    elif testtype == 7:
        multi_dip_test()


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
            numfail += schedule_tasks(utilization, period, 3)
        accRatios.append(1 - (numfail / numsets))
        print("Total utilization:", z, "=> Num of fails: ", numfail, " Acceptance ratio: ", 1 - (numfail / numsets))
        z += utilstep
    plotgraph(accRatios, utils, False)
    exit()


def edf_cust(fperiod, speriod):
    z = 0
    accRatios = []
    # utils = []
    while z <= 100:
        # utils.append(z)
        numfail = 0
        for x in range(numsets):
            utilization = drs(numtasks, z / 100)
            period = [fperiod, speriod]
            numfail += schedule_tasks(utilization, period, 3)
        accRatios.append(1 - (numfail / numsets))
        # print("Total utilization:", z, "=> Num of fails: ", numfail, " Acceptance ratio: ", 1 - (numfail / numsets))
        z += utilstep
    # plotgraph(accRatios, utils, False)
    return accRatios


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
            # utilization.sort()
            for i in range(variations):
                period = [primperiod, primperiod + (i * periodstep)]
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
            if both:
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


def quantity_test():
    z = 0
    print("Testing EDF-Like Algorithm with implicit deadlines and dynamic priority(EDF). Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatios = []
    utils = []
    while z <= 100:
        utils.append(z)
        failset = [0, 0, 0]
        for i in range(3):
            numfail = 0
            n = numtasks + (i*numtaskstep)
            for x in range(numsets):
                utilization = drs(n, z / 100)
                period = loguniform(n)
                numfail += schedule_tasks(utilization, period, 3)
            failset[i] = round(1 - (numfail / numsets), 2)
        accRatios.append(failset)
        print("Total utilization:", z, "=> Acceptance ratio: ", failset)
        z += utilstep
    plotgraph(accRatios, utils, True)
    exit()


def const_deadline():
    # tasks = [[10, 3, 5], [12, 7, 12], [30, 8, 20]]
    # result = pda.pda(tasks)
    # print(result)

    z = 0
    print("Testing EDF-Like Algorithm with constraint deadlines and dynamic priority(EDF). Number of task sets:",
          numsets, "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatio_el_edf = []
    accRatio_el_dm = []
    accRatio_pda = []
    accRatio_suf = []
    utils = []
    period = []
    count = 0
    for j in range(numtasks):
        period.append(pow(2, j+1))
    while z <= 100:
        utils.append(z)
        numfail_pda = 0
        numfail_suf = 0
        numfail_el_edf = 0
        numfail_el_dm = 0
        for x in range(numsets):
            if z == 0:
                utilization = drs(numtasks, 0.01 / 100)
            else:
                utilization = drs(numtasks, z / 100)
            deadline = [i * ppercentage for i in period]
            numfail_el_edf += schedule_tasks(utilization, period, 3, deadline)
            numfail_el_dm += schedule_tasks(utilization, period, 2, deadline)
            execution = [utilization[i] * period[i] for i in range(len(utilization))]
            pdatasks = []
            for m in range(len(utilization)):
                pdatasks.append([period[m], execution[m], deadline[m], utilization[m]])
            if not pda.pda(pdatasks):
                numfail_pda += 1
            if not cd_suff_test(pdatasks):
                numfail_suf += 1
        count += 1
        accRatio_el_edf.append(1 - (numfail_el_edf / numsets))
        accRatio_el_dm.append(1 - (numfail_el_dm / numsets))
        accRatio_pda.append(1 - (numfail_pda / numsets))
        accRatio_suf.append(1 - (numfail_suf / numsets))
        print("Total utilization:", z, "=> Num of fails: (EL-edf)", numfail_el_edf, "(EL-dm)", numfail_el_dm, "(PDA)",
              numfail_pda, "(Sufficient Test)", numfail_suf, "; Acceptance ratio: (EL-edf)",
              round((1 - (numfail_el_edf / numsets)), 2), "(EL-dm)", round((1 - (numfail_el_dm / numsets)), 2), "(PDA)",
              round((1 - (numfail_pda / numsets)), 2), "(Sufficient Test)", round((1 - (numfail_suf / numsets)), 2))
        z += utilstep
    plotgraph([accRatio_el_edf, accRatio_el_dm, accRatio_pda, accRatio_suf], utils, False)
    exit()


def cd_suff_test(tasks):
    tasks.sort(key=lambda n: n[2])              # Sort task set by deadline
    for k in range(len(tasks)):
        sum_U = 0
        sum_G = 0
        for i in range(k):
            task = tasks[i]
            sum_U += task[3]
            sum_G += (task[1]*(task[0]-task[2])) / task[0]
        result = sum_U + ((1/tasks[k][2]) * sum_G)
        if result > 1:
            return False
    return True


def multi_dip_test():
    m = 1
    totalaccratio = []
    a_points = []
    a_slide = periodstep/primperiod
    print(a_slide)
    while m <= aparam:
        result = edf_cust(primperiod, primperiod * m)
        result = round(sum(result), 2)
        totalaccratio.append(round(result / ((100/utilstep)+1), 3))
        a_points.append(m)
        m = round(m + a_slide, 3)
    print(totalaccratio)
    print(a_points)
    plotgraph(totalaccratio, a_points, False)


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


def plotgraph(a, u, mul):
    if mul:
        if testtype == 4:
            for x in range(3):
                arr = []
                for i in range(len(a)):
                    arr.append(a[i][x])
                plt.plot(u, arr, label="Tasks #: " + str(numtasks+(x*numtaskstep)))
                plt.scatter(u, arr)

        # markers = ["o", ",", "v", "^", "<", ">"]
        else:
            for x in range(variations):
                arr = []
                for i in range(len(a)):
                    arr.append(a[i][x])
                plt.plot(u, arr,
                         label=str(primperiod+(x*periodstep))+" (" + str(round((x * periodstep * 100)/primperiod))+"%)")
                plt.scatter(u, arr)
        plt.xlabel('Utilization (%)')
        plt.ylabel('Acceptance Ratio')
        plt.legend(loc="lower left")
        plt.yticks(arange(1.1, step=0.10))
        plt.xticks(arange(101, step=10))
        plt.show()
    else:
        if testtype == 5:
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
                bound = numtasks * (pow(2, 1 / numtasks) - 1)
                plt.axvline(x=bound * 100, color='r')
            if both:
                plt.plot(u, a[2])
                plt.scatter(u, a[2])
            plt.show()
        elif testtype == 6:
            names = ["EL-EDF", "EL-DM", "PDA", "Sufficient Test"]
            for i in range(4):
                plt.plot(u, a[i], label=names[i])
                plt.scatter(u, a[i])
            plt.title("Constraint Deadline with " + str(ppercentage*100) + "%")
            plt.xlabel('Utilization (%)')
            plt.ylabel('Acceptance Ratio')
            plt.yticks(arange(1.1, step=0.10))
            plt.xticks(arange(101, step=10))
            plt.legend(loc="lower left")
            plt.show()
        elif testtype == 7:
            plt.plot(u, a)
            plt.scatter(u, a)
            plt.xlabel('Change of \'a\'')
            plt.ylabel('Total Acceptance Ratio')
            plt.xticks(arange(1, aparam+1, 1))
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
    parser.add_argument("-pp", "--primaryperiod", dest="pperiod", type=int, default=1,
                        help="Specify the primary period to be used for the edf dip analysis")
    parser.add_argument("-ps", "--periodstep", dest="pstep", type=int, default=0,
                        help="Specify the period step for the dip analysis")
    parser.add_argument("-v", "--variations", dest="var", type=int, default=2,
                        help="Specify the amount of plots to be created.")
    parser.add_argument("-nts", "--numtaskstep", dest="ntstep", type=int, default=0,
                        help="Specify the amount of change for the number of tasks per task set.")
    parser.add_argument("-cd", "--constdead", dest="cdead", type=float, default=0.9,
                        help="Specify the percentage of the periods to be used for constraint deadlines.")
    parser.add_argument("-a", "--aparam", dest="a", type=int, default=2,
                        help="Specify the a parameter for the multi-dip test.")
    parser.add_argument("-b", "--both", dest="both", type=int, default=False, help="Show both tests.")
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
    both = args["both"]
    seed = args["seed"]

    random.seed(seed)

    if testtype == 3 or testtype == 7:
        numtasks = 2

    # Example of execution in terminal:
    # python3 EL_testing.py -tt 1 -ts 20 -nt 5 -us 10

    # For edf-dip, number of tasks should always be equal to 2
    # Also the period step should be given: python3 EL_testing.py -tt 3 -ts 10 -nt 2 -us 5 -pp 100 -ps 80 -v 10 -s 1

    # For TDA test the el algorithm with dynamic priority can also be included into the graph by using the arg --both
    # Like so: python3 EL_testing.py -tt 5 -ts 10 -nt 10 -us 5 -b 1 -s 5

    # For quantity of tasks per task set test:
    # python3 EL_testing.py -tt 4 -ts 20 -nt 5 -us 5 -nts 10 -s 2

    # For multi dip test(Number of tasks = 2):
    # python3 EL_testing.py -tt 7 -ts 100 -nt 2 -us 5 -pp 100 -ps 20 -a 5 -s 2

    # For constraint deadline test with PDA:
    # python3 EL_testing.py -tt 6 -ts 100 -nt 10 -us 5 -cd 0.6 -s 2

    main()
