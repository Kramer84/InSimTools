# InSimTools
High level methods built for LFS

## This readme is more of a note - ***Ongoing project***

- As pyinsim is a relatively low-level and complex package, the goal here is to expose more functionalities and garantee
  more convenient access to the base level methods. An object oriented paradigm is chosen here. 
  
- The idea will be to separate the different insim functionalities in classes, and define a templated basic behaviour. 

- A first idea is that InSim handling can be separated in two main type of actions/events:
    - Handling / Listening events: Contains all the functions listening to LFS events and launching callback functions in response 
    - Action Class : All the functions acting on the behaviour of LFS
    
The aim of the Handler class will be to have a specific handler method for each and every event LFS could send. Each handler 
method will be linked to a callback function situiated in a other file. These callback functions will define 
the behaviour of LFS and be custom. Of course the handler class will try to expose in the clearest way possible the data that is sent over by LFS.

The aim of the action class will be to explicitely expose all the functions acting on LFS, as well as the ones allowing
to precisely gather data.


Of course, these basic ideas ar just the first layer for this project. The handling classes can potentially be separated into 
connection / race related events, to separate the different ideas of sim racing behaviour control.  
