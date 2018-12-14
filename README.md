# BE 223A Course Project

Course name: Bioengineering 223A - Programming Laboratory for Medical and Imaging Informatics I

Instructor: William Speier 

This course project aims to develop an application that automatically generates 3D brain surfaces with color labeling based on underlying neurological signals. 

## Getting Started

These instructions will help you get the application up and running on your local machine.

### Prerequisites

- BrainSuite 18a 
    - Download the most recent version of BrainSuite from their website: http://forums.brainsuite.org/download/
    - Login required for downloading
- Python 3.6
    - Download Python from their website: https://www.python.org/downloads/
    - Dependencies
        - postgresql, psycopg2, psycopg2.extras, psycopg2.extensions, config, os, sys, csv, pandas, scipy, numpy, nibabel, mayavi, PyQt5, SimpleITK, math, traits

### Installation and setup



```

```


```

```


```

```


### Running the program


```

```


```

```

```

```


### Formats of input and output files

- Signal processing 
    - Channel importance
        - Input: EEG CSV file
        - Output: scores list
    - Channel-qc
        - Input: EEG CSV file
        - Output: channel list with value ranging 0 (bad) - 1 (good)
    - Speech correlation
        - Input: ECoG signal file (.dat)
        - Output: Time shift for each channel to database
    - Band power over time
        - Input: BCI2000.dat or EDF file
        - Output: CSV file
    - Phase amplitude coupling (PAC)
    - Input: BCI2000.dat (EEG and ECOG methods), EDF Files
        - Output: CSV File
        
- Electrode localization
    - CT->MR registration
        - Input: pre-operative MRI image & post-operative CT image (both in NIfTI format)
        - Output: registered CT image (NIfTI format)
    - Electrode detection
        - Input: registered CT image (NIfTI format)
        - Output: channel coordinates in MR space in 3 separate Lists (x,y,z)
    - Talairach->MR registration
        - Input: Talairach channel coordinates in .csv format
        - Output: channel coordinates in MR space 3 separate Lists (x,y,z)

- Surface reconstruction
    - Skull-stripping (only for ECoG subjects)
        - Input: Preop head MRI NIfTI file
        - Output: Skull-stripped cerebrum mask NIfTI file
    - Electrode position correction (only for ECoG subjects)
        - Input: electrode coordinates from database 
        - Output: update the database with the corrected coordinates
    - ECoG labeling:
        - Input: JPG file
        - Output: write channel labels to database
    - Heatmap generation:
        - Input: scores (EEG/ECoG), coordinates (EEG/ECoG), brain mask (skull stripped) from database
        - Output: plot windows

Notes:
1. EEG subjects will use the cerebrum mask from a standard subject to plot. The data has been prestored in the database. 
2. Electrode coordinates for EEG subjects are predetermined and are prestored in the database. 
    
## Authors

All contributors have worked collaboratively on this project.  

## License



## Acknowledgments

We thank Dr. Speier for his guidacne during the course of building this application.  
