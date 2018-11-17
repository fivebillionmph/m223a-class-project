import psycopg2
from config import config

# add stripped skull file path into subjects table
# input: text of smr file path resulting from Skull-stripping.py
    # expected path: C:\Users\aa\Desktop\T1.nii.gz_cerebrum.mask.nii.gz

def insert_subject_smr(smr_path):
    """ insert the SMR filepath into the subjects table """
    sql = """INSERT INTO subjects(smr_path) VALUES(%s);"""
    conn = None
    sid = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (smr_path,))
        # get the generated id back
        sid = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
 
    return sid