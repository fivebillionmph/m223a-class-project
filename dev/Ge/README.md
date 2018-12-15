 Speech Correlation
 ======
 Ge Fang
 ## Goals
 
Function 1: Finding Channel contributed to vocal cord control by bandpower analysis

## Pipelines
### Function 1
The function of speech correlation(method_5.py) will be run separately by call it on python or cmd. The user can call “method 5” in brainsweet for the command of below:

1. Get the path of The ECoG file the user want to analyse, which will be saved as a local text file ‘method5_ECoG_path.txt’.
2. Upload the existed result of method 5 to database: if the users is running brainsweet, and they want to update the result they got earlier to the database, they can type in the SID, and also the path of the result CSV file under instruction.


**Input**: ECOG001.dat

**Output**: 
>csv file: correlation table(scores)

>plot(multiple frequency): 
>* x-axis: channel number
>* y-axis: time-delay

 ## Updates
* uploading python files of workable functions
 ## Future
1. debug new functions and upload
2. modify output file(.csv, .jpg)
3. wrap .py into .exe
4. work with database


## Installment Requirements:

### Python 3.6
#### Package needed:
* numpy
* scipy.fftpack
* matplotlib.pyplot
* importlib
* sys
* os




