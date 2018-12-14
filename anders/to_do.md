## TASKS TO COMPLETE

#### Signal processing
* incorporate Audio signal processing component (Ge)
    * add component call to the project wrapper as analysis method 5
    * suggestion: figure out how to get the audio processing running in parallel, as soon as the file is available, given the 
    extensive amount of time it takes to run this component.
* ensure that Jake's method runs without update to Python 3.6-specific .exe
* resolve .dat vs .csv discrepancy (Amy, David, Jake, Mohammad)
    * request .dat file from user and convert to .csv where needed
    * Amy and David (methods 1 and 2) use .csv as input
        * add .dat->.csv conversion to these with if statement
    * Jake and Mohammad (methods 3 and 4) use .dat as input
    * perhaps, since these methods are supposed to be called for different experiment types, we could restrict methods 
    1+2 to EEG expts and methods 3+4 to ECoG expts.
#### Heat map
* test functionality to display multiple signal analyses 
* run further tests on classroom computer

