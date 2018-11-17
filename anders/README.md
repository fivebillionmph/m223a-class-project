## database integration

#### purpose: establish database structure


#### language: python 3.6
#### dependencies: postgresql, psycopg2, psycopg2.extras, psycopg2.extensions, config

#### database specifics:
    - host='localhost'
    - dbname='brain_db'
    - user='postgres'
    - password='pass'

#### initial inputs:
    - eeg channel coordinates (hard coded .csv)
    - UI should request file locations from user for:
        - mri (NIFTI)
        - ct (NIFTI)
        - eeg signal files (BCI2000)
        - ecog signal files (BCI2000, EDF)
    	- ecog channel map (JPG)

#### outputs:
    - provide file location for: 
        - mri (NIFTI)
        - ct (NIFTI)
        - smr (NIFTI)
        - signal files (BCI2000, EDF)
    	- ecog channel map (JPG) 
    - provide data direct from db:
    	- ecog channel coordinates (.csv)
    	- eeg channel coordinates (.csv)
    	- channel scores (.csv)

#### intermediary inputs:
    - file location of smr
    - ecog channel coordinates (.csv)
    - channel scores (.csv)