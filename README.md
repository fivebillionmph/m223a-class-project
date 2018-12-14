# BE 223A Course Project

Course name: Bioengineering 223A - Programming Laboratory for Medical and Imaging Informatics I

Instructor: William Speier 

This course project aims to develop an application that automatically generates 3D brain surfaces with color labeling based on underlying neurological signals. 

## Getting Started

These instructions will help you get the application up and running on your local machine.

### Prerequisites

- BrainSuite 18a 
    - Download the most recent version of BrainSuite from their website: http://forums.brainsuite.org/download/
    - A free login account must be established before downloading
- PostgreSQL 11
    - Download the most recent version (11) from the postgresql website: https://www.postgresql.org/
- Python 3.6
    - Download Python from their website: https://www.python.org/downloads/
    - Dependencies
        - postgresql, psycopg2, psycopg2.extras, psycopg2.extensions, config, os, sys, csv, pandas, scipy, numpy, 
        nibabel, mayavi, PyQt5, SimpleITK, math, traits
- 

### Installation and setup
- create 'brain_db' database with recreate_db.py script in the main program folder
    - run this script only once! This deletes any currently existing database with the name 'brain_db', allowing a 
    fresh start on an empty database, if desired.
    - any connections to the database must be closed to run this script
    - database specifics:
        - host='localhost'
        - dbname='brain_db'
        - user='postgres'
        - password='pass'
- establish database schema with build_schema.py script (found in /db_setup)
    - run this script only once! This must be a fresh instantiation of the brain_db database, which can be accomplished 
    by running the previously discussed recreate_db.py script.
    - creates 5 relations:
        - subjects: sid, name, type, ct_path, mr_path, rct_path, smr_path
        - signals: sid, signal_path
        - channels: sid, channel, eid, x, y, z
        - scores: sid, channel, method, score[1:100]
        - eeg: eid, eeg_name, x, y, z
    - fills eeg relation with standard 10-20 eeg coordinates



### Running the program
- run wrapper.py to fill tables with subject information, experiment details, and file paths, and to call each component
for image processing and signal analysis
    - requests subject name and experiment type (EEG or ECoG)
    - if ECoG, requests file paths for MR and CT images, signal files
    - if EEG, requests file paths for MR images and signal files

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
