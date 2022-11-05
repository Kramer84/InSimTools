# InSimTools
High level methods built for LFS

## This readme is more of a note - ***Ongoing project***

- As pyinsim is a relatively low-level and complex package, the goal here is to expose more functionalities and garantee
  more convenient access to the base level methods. An object oriented paradigm is chosen here.

- The idea will be to separate the different insim functionalities in classes, and define a templated basic behaviour.

- A first idea is that InSim handling can be separated in two main type of actions/events:
    - Handling / Callback events: Contains all the functions listening to LFS events and launching callback functions in response
    - Requests  :  All possible requests possible to sent to LFS exposed in explicit methods.

The aim of the Handler class will be to have a specific handler method for each and every event LFS could send. Each handler method can be linked to a callback function situiated in a other file. These callback functions will define the behaviour of LFS and be custom. Of course the handler class will try to expose in the clearest way possible the data that is sent over by LFS.

Also implemented is a Live Data tracker, which exposes and stores the connection/player/map/server data in a dedicated object, and updates it via callbacks and requests.

## To get starting :
All of this was testes on a Windows 10 machine, but it shouldn't be too different on Linux. Tests were done using Python 3.10.6

If you aren't so familiar with Python I would recommend you follow these steps :

- Download the latest [Anaconda](https://www.anaconda.com/products/distribution) and install using the standard procedure.

- Download the pyinsim source files (for now from [this fork](https://github.com/Kramer84/pyinsim-python3-porting), as all was not yet merged with [Alex McBrides](https://github.com/alexmcbride/pyinsim) work.)

- Create a [conda virtual environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) using commands in the **Anaconda Bash** application, having *numpy*, *pandas*, and maybe some other basic packages. Those are not required for these scripts (for the moment).

- Go to the pyinsim source folders in Anaconda Bash, with your environment activated, and launch one of the commands found in the README, this should install pyinsim.

- Then to start testing,