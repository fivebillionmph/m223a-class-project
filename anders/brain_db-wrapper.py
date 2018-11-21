# requests subject name and populates subject table.
# requests initial file inputs from the user.

import psycopg2
import psycopg2.extras
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
            mr_path = input("What is the MR file path? ")

        ct=input("Do you have a CT file for this subject? (y/n) ")   
        if ct == "y":
            ct_path = input("What is the CT file path? ")
        else:
            ct_path = input("What is the excel file path with electrode coords? ")
    
    # insert subject data into subjects relation based on acquisitions from user.
    insert_subject = """INSERT INTO subjects(name,type,mr_path,ct_path) VALUES(%s,%s,%s,%s) RETURNING sid;"""
    cursor.execute(insert_subject, (name,expt_type,mr_path,ct_path))        
    # get subject ID
    sid = cursor.fetchone()["sid"]

else:
    sid = subject_names[0]["sid"]
    
# commit the transaction
conn.commit()

# request first signal file path: 
signal_path1 = input("Please enter the first signal file path. ")

eeg_file = input("Please enter the first EEG signal file path. ")

# in development: request second signal file path:
#sig2 = input("Do you have another signal file? (y/n) ")
#if sig2 == "y":
#    signal_path2 = input("Please enter the second signal file path. ")

insert_signals = """INSERT INTO signals(sid,signal_path) VALUES(%s,%s) RETURNING sid;"""
cursor.execute(insert_signals, (sid,signal_path1))

# commit the transaction
conn.commit()


cursor.execute("SELECT * FROM subjects WHERE sid = %s", (sid,))
subject_row = cursor.fetchall()[0]

print(sid)
mr_path = subject_row["mr_path"]
ct_path = subject_row["ct_path"]

# run each individual user's scripts
Yannan.run(cursor, sid, config.brainsuite_cortical_extraction_script, mr_path)

if config.is_windows:
    Jake.run(cursor, "test", "0", "100", "0", "100")

Joseph.run(cursor, sid, ct_path, mr_path)
David.run(cursor, sid, eeg_file)
Amy.run(cursor, sid, eeg_file)

# Jake has two methods: one for EDF and one for DAT
    # can specify time ranges and frequency bands of expt 
    # results in different scores (to be added as JakeMethod1a, JakeMethod1b)
    # method name might take format: "Jake_[time sequence]_[frequency band]"
    # will have to prompt user to specify their time ranges and frequency band

# close the database communication
cursor.close()
