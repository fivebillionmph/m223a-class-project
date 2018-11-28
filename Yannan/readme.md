## Skull-stripping & Electrode Position Correction

#### Electrode Posistion Correction

#### Input
- ECoG coordinates from CT-MR registration: request data from database channel table
- MR iamge data: request from database subject table

#### Output
- Corrected coordinates for channel plotting
- Upload corrected coordinates back to database

#### Language 
- Python 2.7

#### Required Python Packages
- math

#### Additional Notes
- This script is used for preventing electrodes from floatting around the cortical surface. If any electrode was found to be not well plotting on the cortical surface, the coordinates of this electrode would be corrected automatically by this program.

#### Skull-stripping

#### BrainSuite Batch Processing
- Python calls command line to run BrainSuite 
- Reference: http://brainsuite.org/wp-content/uploads/2017/06/BrainSuite_Workshop_2017_Batch_David_Shattuck.pdf

#### Input
- MR Image data file
- File format: NIfTI 
  
#### Output
- Skull-stripped NIfTI file
- Use the one ending with "_cerebrum.mask.nii.gz" 

#### Language
- Python 2.7 or 3.7

#### Required Python Packages
- os

#### Requried Software
- BrainSuite 18a

#### Operating Systems
- Mac
- Windows

#### Additional Notes

- Once BrainSuite runs, it will take more than 5 minutes to finish as skull-stripping through BrainSuite can take up to 20 minutes depending on the input file. During skull-stripping, a handful of files will be generated and the only one will be used for channel plotting is filename.cerebrum.mask.nii.gz. This file will be generated shortly (usually less than one minute) after running the python script. 

- According to the testing I have done on Mac and PC, BrainSuite runs faster on Mac than on Windows machine. Becasue we will run our script on a Windows machine for the final demo, we would expect BrainSuite to run at least 10 miniutes to get the filename.cerebrum.mask.nii.gz file we need.

- Channel plotting is incorporated in the heat map step, therefore, the codes do not need to be uploaded for the beta version demo.
