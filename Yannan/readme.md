## Skull-stripping and Channel Plotting

#### Components:
- Skull-stripping_EEG.py
- Skull-stripping_ECoG.py
- EEG_Channel_Plotting.py
- ECoG_Channel_Plotting.py

#### Inputs:
- Skull-stripping
 - File: MR Image data file
 - File format: NIfTI 
- Channel plotting 
 - File: Coordinates of electrodes
 - File format: Excel
  
#### Outputs:
- Skull-stripping
 - Skull-stripped NIfTI file
- Channel plotting
 - Brain mask with electrodes on the surface

#### Language:
- Python 2.7

#### Required Python Packages
- psycopg2
- nibabel
- mayavi
- xlrd
- os

#### Requried Software
- BrainSuite 18a

#### Additional Notes
- Once Skull-stripping_EEG.py or Skull_stripping_ECoG.py runs, it will take more than 5 minutes to finish as skull-stripping through BrainSuite can take up to 20 minutes depending on the input file. During skull-stripping, a handful of files will be generated and the only one will be used for channel plotting is filename_cerebrum.mask.nii.gz. This file will generate shortly (usually less than one minute) after running the python script. 
