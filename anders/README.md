## database integration

#### purpose: establish database structure

#### instructions:
- create 'brain_db' database with recreate_db.py script in the main folder
    - deletes any currently existing database with the name 'brain_db'
    - all connections to the database must be closed to run this script
- establish database schema with build_schema.py script (found in /db_setup)
    - creates 5 relations:
        - subjects: sid, name, type, ct_path, mr_path, rct_path, smr_path
        - signals: sid, signal_path
        - channels: sid, channel, eid, x, y, z
        - scores: sid, channel, method, score[1:100]
        - eeg: eid, eeg_name, x, y, z
    - fills eeg relation with standard 10-20 eeg coordinates
- run wrapper.py to fill tables with subject data
    - requests subject name and experiment type (EEG or ECoG)
    - if ECoG, requests file paths for mri, ct, channel map files
    - if EEG, requests 

#### language: python 3.6
#### dependencies: postgresql, psycopg2, psycopg2.extras, psycopg2.extensions, config

#### database specifics:
- host='localhost'
- dbname='brain_db'
- user='postgres'
- password='pass'

#### initial inputs:
- mri (NIFTI) (standard brain if none provided)
- ct (NIFTI)
- subject-specific eeg channel names (.csv)
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

