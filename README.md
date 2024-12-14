# Repository for my Bachelor Thesis "Towards Exact Analysis of EDF-Like Scheduling"
This repository was created to share the code used to evaluate the exactness of the algorithm for scheduling tasks, namely EDF-Like Scheduling. The algorithm's original repository can be found [here](https://github.com/tu-dortmund-ls12-rt/EDF-Like). The main file that can be used to test the algorithm is _El_testing.py_ which is located in the folder _EDF_Like_. The test essentially generates task sets first and then calls EDF-Like scheduling to schedule the tests. The resulting data is then accordingly plotted so that the schedulability can be analyzed. More on how the tests were conducted and the outcomes can be found [here](https://daes.cs.tu-dortmund.de/de/beschaeftigte/wissenschaftliche-mitarbeiter/msc-mario-guenzel/).

### Requirements

To run the tests [Python3.10](https://www.python.org/downloads/release/python-3100/) has to be installed on the machine.
Moreover, the following Python packages are required:

```
matplotlib
numpy
drs
```

Assuming that Python 3 is installed in the targeted machine, to install the required packages:

```
python3 -m pip install matplotlib numpy drs
```

In case any dependent packages are missing, please install them accordingly.

## How to run the Tests
The individual tests can be run by calling the El_testing.py file from the terminal and passing the corresponding arguments. Once the plot(s) are generated, they are saved as either outcome_1.jpg or outcome_2.jpg in the same file directory where El_testing.py is located. Also, it is important to know that not all arguments must be used for each test.

### Available Arguments
- tt  - specifies the test that will be executed. Available options are numbers 1 to 7
- ts  - specifies the number of task sets to be generated
- nt  - specifies the number of tasks in a task set
- us  - specifies the utilization step between the individual runs. This means with a utilization step of 20, the test will be executed at the following utilization levels: [0, 20, 40, 60, 80, 100]
- pp  - specifies the primary period used when testing the schedulability under period variation. The period of the first task of the two tasks in the task set is set to this value
- ps  - specifies the period step used when testing the schedulability under period variation, meaning the period of the second task of the two tasks, will increase by this given value every run.
- v   - specifies how many runs should be executed for testing
- nts - specifies the number of tasks to be added, in other words, the task number step
- cd  - specifies the percentage that will be taken from the periods to create constrained-deadline task sets
- a   - specifies the 'a' parameter introduced in the thesis (_T_2 = a *T_1_)
- co  - specifies which configuration of EDF-Like should be used. Available options are 2 (EL-DM) and 3 (EL-EDF)
- s   - specifies the seed used for the random number generator  

### Available Tests
**Utilization-based test**  
This test gives out a plot with one run with the specified EDF-Like configuration

Example with `python3 EL_testing.py -tt 1 -ts 20 -nt 5 -us 10 -co 3 -s 0`:
[![output-1.jpg](https://i.postimg.cc/0534nDb3/output-1.jpg)](https://postimg.cc/Rq7GV31Q)

**Advanced Utilization-based test**  
This test gives out a plot with three runs (TDA, EL-DM, EL-EDF). Also as a benchmark, the Liu and Layland bound is shown.

Example with `python3 EL_testing.py -tt 5 -ts 10 -nt 10 -us 5 -s 0`:
[![output-1.jpg](https://i.postimg.cc/vTZtdQ3D/output-1.jpg)](https://postimg.cc/KkCMPyXy)

**Period variation test (util-based plotting)**  
This test focuses on showing the effects on the schedulability when increasing the period of another task. Therefore there are only two tasks per task set. The outcome is a plot with _v_ runs, where with each subsequent run, the second task's period increases by the _ps_ value given. Both tasks at the first run have a period of the given _pp_ value.

Example with `python3 EL_testing.py -tt 3 -ts 10 -nt 2 -us 5 -pp 100 -ps 80 -v 10 -co 3 -s 0`:
[![output-1.jpg](https://i.postimg.cc/Z5ZzPpQm/output-1.jpg)](https://postimg.cc/9rxkCRVg)

**Period variation test (different approach)**
This test is similar to the one above, the only difference being the way the resulting data will be plotted ()


**Quantity of tasks per task set variation test**  
This test focuses on showing the impact of changing the number of tasks per task set. The outcome is two plots, the first is the ordinary util-based plotting and the second is the different approach(total acceptance ratio as a function of the number of tasks per set).

Example with `python3 EL_testing.py -tt 4 -ts 20 -nt 5 -us 5 -v 4 -nts 10 -co 3 -s 0`:
[![output-1.jpg](https://i.postimg.cc/Z5ZzPpQm/output-1.jpg)](https://postimg.cc/9rxkCRVg)

[![output-2.jpg](https://i.postimg.cc/bYWznG8Y/output-2.jpg)](https://postimg.cc/ThjMM3pB)




## Recreation of Conducted Tests from Thesis


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
