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
The individual tests can be run from the terminal by passing the corresponding arguments. Also, it is important to know that not all arguments must be used for each test.

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
**Utilization-based test, without TDA**

Example with `python3 EL_testing.py -tt 1 -ts 20 -nt 5 -us 10 -co 3 -s 0`:

![Screenshot of a comment on a GitHub issue showing an image, added in the Markdown, of an Octocat smiling and raising a tentacle.](https://ibb.co/XL32d35)

## Recreation of Conducted Tests from Thesis


## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
