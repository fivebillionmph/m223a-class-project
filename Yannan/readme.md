## Skull-stripping 

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

#### Additional Notes
- Once BrainSuite runs, it will take more than 5 minutes to finish as skull-stripping through BrainSuite can take up to 20 minutes depending on the input file. During skull-stripping, a handful of files will be generated and the only one will be used for channel plotting is filename_cerebrum.mask.nii.gz. This file will be generated shortly (usually less than one minute) after running the python script. 
