import psycopg2
#from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

name=input("Please enter subject name.")

conn=psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
#conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor()

sql = """SELECT sid from subjects WHERE name=%s"""
cursor.execute(sql, (name,))

subject_names = cursor.fetchall()

if len(subject_names) == 0:
    expt_type=input("Please enter experiment type (EEG/ECoG).")
    # add a 'while' loop to demand only EEG or ECOG as input.
    
    # hard coded path to standard brain MR
    mr_path = "/data/T1.nii.gz"    
    ct_path = ""
    
    if expt_type == "ECoG":
        mr=input("Do you have an MR file for this subject? (y/n)")
        if mr == "y":
            mr_path = input("What is the MR file path?")

        ct=input("Do you have a CT file for this subject? (y/n)")   
        if ct == "y":
            ct_path = input("What is the CT file path?")
        else:
            ct_path = input("What is the excel file path with electrode coords?")
        
    sql = """INSERT INTO subjects(name,type,mr_path,ct_path) VALUES(%s,%s,%s,%s) RETURNING sid;"""
    cursor.execute(sql, (name,expt_type,mr_path,ct_path))        
    # get subject ID
    sid = cursor.fetchone()[0]

else:
    sid = subject_names[0][0]
    
# commit the transaction
conn.commit()
# close the database communication
cursor.close()

print(sid)