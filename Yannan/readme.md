## Skull-stripping 

#### Input
- MR Image data file
- File format: NIfTI 
  
#### Output
- Skull-stripped NIfTI file

#### Language:
- Python 2.7

#### Required Python Packages
- psycopg2
- nibabel
- xlrd
- os

#### Requried Software
- BrainSuite 18a

#### Additional Notes
- Once BrainSuite runs, it will take more than 5 minutes to finish as skull-stripping through BrainSuite can take up to 20 minutes depending on the input file. During skull-stripping, a handful of files will be generated and the only one will be used for channel plotting is filename_cerebrum.mask.nii.gz. This file will generate shortly (usually less than one minute) after running the python script. 
- EEG electrode coordinates also need to be uploaded to database beforehand.
