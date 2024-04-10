from schedTest import EL
from drs import drs
import random
import math
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from numpy import arange

numsets = 1
seed = 0


def main():
    n = numtasks
    z = 0
    print("Testing EDF-Like Algorithm with implizit deadlines. Number of task sets:", numsets,
          "| Number of tasks per set:", numtasks, "| Utilization step:", utilstep)
    accRatios = []
    utils = []
    while z <= 100:
        utilization = drs(n, z/100)
        utils.append(z)
        z += utilstep
        numfail = 0
        for x in range(numsets):
            tasks = []
            period = loguniform(n)
            # print(period)
            execution = [utilization[i] * period[i] for i in range(len(utilization))]
            sumU = 0
            for y in range(n):
                tasks.append(
                    {'period': period[y], 'execution': execution[y], 'deadline': period[y],
                     'utilization': utilization[y], 'sslength': 0})
                sumU += utilization[y]
            sortedtasks = sorted(tasks, key=lambda item: item['period'])
            if not EL.EL_fixed(sortedtasks, setprio=3):
                numfail += 1
        accRatios.append(1 - (numfail / numsets))
        print("Total utilization:", format(sumU, ".2f"), "=> Num of fails: ", numfail,
              " Acceptance ratio: ", 1 - (numfail / numsets))
    # print(accRatios)
    # print(utils)
    plotgraph(accRatios, utils)
    exit()


def plotgraph(a, u):
    plt.plot(u, a)
    plt.scatter(u, a)
    plt.xlabel('Utilization (%)')
    plt.ylabel('Acceptance Ratio')
    plt.yticks(arange(1.1, step=0.10))
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
    parser.add_argument("-ts", "--tasksets", dest="tsets", type=int, default=1, help="Specify the number of task sets.")
    parser.add_argument("-nt", "--numoftasks", dest="ntasks", type=int,default=10, help="Specify the number of tasks in a task set.")
    parser.add_argument("-us", "--utilstep", dest="ustep", type=float, default=10, help="Specify the utilization step.")
    parser.add_argument("-s", "--seed", dest="seed", type=int, default=200, help="Specify seed for random generation.")
    args = vars(parser.parse_args())

    numsets = args["tsets"]
    numtasks = args["ntasks"]
    utilstep = args["ustep"]
    seed = args["seed"]

    random.seed(seed)

    main()


