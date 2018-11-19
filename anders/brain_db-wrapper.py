# requests initial file inputs from the user, as well as subject name and type

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from mod import config, Yannan

name=input("Please enter subject name. ")

conn=psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor()

select_subject = """SELECT sid from subjects WHERE name=%s"""
cursor.execute(select_subject, (name,))

subject_names = cursor.fetchall()

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

# developing signal insertion: 

# insert_signals = """INSERT INTO signals(sid,signal_path) VALUES(%s,%s) RETURNING sid;"""
# cursor.execute(insert_signals, (sid,signal_path))



# close the database communication
cursor.execute("SELECT * FROM subjects WHERE sid = %s", (sid,))
subject_row = cursor.fetchall()[0]
cursor.close()

print(sid)

mr_path = subject_row[4]
Yannan.run(config.brainsuite_cortical_extraction_script, mr_path)
