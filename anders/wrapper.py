# requests subject name and populates subject table.
# requests initial file inputs from the user.

import psycopg2
import psycopg2.extras
import csv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from mod import config, Yannan, Jake, Joseph, David, Amy

# request subject name from user.
name=input("Please enter subject name. ")

# connect to brain_db and establish cursor connection.
conn=psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

# query brain_db for existing subject name and select subject.
select_subject = """SELECT sid from subjects WHERE name=%s"""
cursor.execute(select_subject, (name,))
subject_names = cursor.fetchall()


#### ACQUIRE SUBJECT NAME, EXPT TYPE, FILE INPUTS
# if subject name does not exist, request name, experiment type, and image paths.
if len(subject_names) == 0:
    expt_type=input("Please enter experiment type (EEG/ECoG). ")
    # add a 'while' loop to demand only EEG or ECOG as input.
    
    # hard coded path to standard brain MR, standard brain SMR, standard EEG, blank CT.
    mr_path = "data/standard.nii"
    smr_path = "data/standard.cerebrum.mask.nii.gz"
    ct_path = ""
    eeg_coords = "data/EEG_10-20.csv"

    # acquire file paths based on experiment type and available images.
    if expt_type == "ECoG":
        mr=input("Do you have an MR file for this subject? (y/n) ")
        if mr == "y":
            mr_path = input("Please enter the MR file path: ")

        ct=input("Do you have a CT file for this subject? (y/n) ")   
        if ct == "y":
            ct_path = input("Please enter the CT file path: ")
        else:
            ct_path = input("Please enter the file path with ECoG electrode coordinates: ")
    
    # insert subject data into subjects relation based on acquisitions from user.
    insert_subject = """INSERT INTO subjects(name,type,mr_path,ct_path) VALUES(%s,%s,%s,%s) RETURNING sid;"""
    cursor.execute(insert_subject, (name,expt_type,mr_path,ct_path))        
    # get subject ID
    sid = cursor.fetchone()["sid"]

else:
    sid = subject_names[0]["sid"]
    
# commit the transaction to add content to subject relation.
conn.commit()


#### ACQUIRE SIGNAL FILE PATHS
# request signal file paths and insert them into brain_db. 
signals = []
signal = input("Please enter the first EEG or ECoG signal file path. ")
signals.append(signal)

while signal != 'q':
    # request another signal file path from the user.
    signal = input("Please enter another signal file path, or enter 'q': ")

    # add the signal file paths to the list.
    if signal != 'q':
        signals.append(signal)

insert_signals = """INSERT INTO signals(sid,signal_path) VALUES(%s,%s);"""

# insert user-provided signal paths into signals table.
for path in signal_paths:
    cursor.execute(insert_signals, (sid,path))


#### FILL CHANNEL TABLE WITH COORDINATES FROM EEG TABLE
if expt_type == "EEG":
    # hard coded path to EEG_channel_names.csv (from Box, converted from xlsx).
    with open('data/EEG_channel_names.csv') as subject_eeg:
        eeg_names = csv.reader(subject_eeg)
            
        select_eeg_channel = """SELECT * FROM eeg WHERE LOWER(eeg_name)=LOWER(%s);"""
        insert_eeg_channel = """INSERT INTO channels(sid, channel, eid) VALUES(%s,%s,%s);"""
        
        for row in eeg_names:
            eeg_coords = cursor.execute(select_eeg_channel, (row[1],))
            eeg_row = cursor.fetchall()[0]            
            cursor.execute(insert_eeg_channel, (sid, row[0],eeg_row[0]))

# commit the transaction
conn.commit()


#### RUN INDIVIDUAL COMPONENT SCRIPTS
# SKULL STRIPPING
Yannan.run(cursor, sid, config.brainsuite_cortical_extraction_script, mr_path)
# need to feed output file path to "smr" column of subjects table

# MR/CT ELECTRODE REGISTRATION
if config.is_windows:
    Jake.run(cursor, "test", "0", "100", "0", "100")
Joseph.run(cursor, sid, ct_path, mr_path)


# SIGNAL ANALYSIS
David.run(cursor, sid, eeg_file)
Amy.run(cursor, sid, eeg_file)

# Jake has two methods: one for EDF and one for DAT
    # can specify time ranges and frequency bands of expt 
    # results in different scores (to be added as JakeMethod1a, JakeMethod1b)
    # method name might take format: "Jake_[time sequence]_[frequency band]"
    # will have to prompt user to specify their time ranges and frequency band


# close the cursor and database communication
cursor.close()
conn.close()