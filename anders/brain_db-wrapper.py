# requests subject name and populates subject table.
# requests initial file inputs from the user.

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# request subject name from user.
name=input("Please enter subject name. ")

# connect to brain_db and establish cursor connection.
conn=psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor()

# query brain_db for existing subject name and select subject.
select_subject = """SELECT sid from subjects WHERE name=%s"""
cursor.execute(select_subject, (name,))
subject_names = cursor.fetchall()

# if subject name does not exist, request name, type, 
if len(subject_names) == 0:
    expt_type=input("Please enter experiment type (EEG/ECoG). ")
    # add a 'while' loop to demand only EEG or ECOG as input.
    
    # hard coded path to standard brain MR
    mr_path = "/data/T1.nii.gz"    
    ct_path = ""
    
    if expt_type == "ECoG":
        mr=input("Do you have an MR file for this subject? (y/n) ")
        if mr == "y":
            mr_path = input("What is the MR file path? ")

        ct=input("Do you have a CT file for this subject? (y/n) ")   
        if ct == "y":
            ct_path = input("What is the CT file path? ")
        else:
            ct_path = input("What is the excel file path with electrode coords? ")
        
    insert_subject = """INSERT INTO subjects(name,type,mr_path,ct_path) VALUES(%s,%s,%s,%s) RETURNING sid;"""
    cursor.execute(insert_subject, (name,expt_type,mr_path,ct_path))        
    # get subject ID
    sid = cursor.fetchone()[0]

else:
    sid = subject_names[0][0]
    
# commit the transaction
conn.commit()

# request first signal file path: 
signal_path1 = input("Please enter the first signal file path. ")

# in development: request second signal file path:
#sig2 = input("Do you have another signal file? (y/n) ")
#if sig2 == "y":
#    signal_path2 = input("Please enter the second signal file path. ")

insert_signals = """INSERT INTO signals(sid,signal_path) VALUES(%s,%s) RETURNING sid;"""
cursor.execute(insert_signals, (sid,signal_path1))

# commit the transaction
conn.commit()

# close the database communication
cursor.close()

print(sid)




