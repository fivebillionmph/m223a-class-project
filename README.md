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

### Installing



```

```


```

```

### Running the program


```

```


```

```

### Formats of input and output files

- Signal processing 
    - Channel importance
        - Input:
        - Output: 
    - Channel-qc
        - Input:
        - Output:
    - Speech correlation
        - Input:
        - Output:
    - Band power over time
        - Input:
        - Output:
    - Phase amplitude coupling (PAC)
        - Input:
        - Output:
        
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
        - Input: Preop head MRI in NIfTI format
        - Output: Skull-stripped cerebrum mask in NIfTI foramt
    - Eletrode position correction (only for ECoG subjects)
        - Input: Pull electrode coordinates from the channles table in the database 
        - Output: Update the database with the corrected coordiantes
    - ECoG labeling:
        - Input:
        - Output:
    - Heat map:
        - Input:
        - Output:

Notes:
1. EEG subjects will use the cerebrum mask from a standard subject to plot. The data has been prestored in the database. 
2. Electrode coordinates for EEG subjects are predetermined and are prestored in the database. 
    
## Authors

All contributors have worked collaboratively on this project.  

## License



## Acknowledgments

We thank Dr. Speier for his guidacne during the course of building this application.  
