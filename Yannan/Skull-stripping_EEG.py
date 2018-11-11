#Course Name: BE 223A 18Fall 
#Author Name: Yannan Lin
#Purpose: Skull-stripping through BrainSuite - EEG

#connect to database
import psycopg2

conn = psycopg2.connect("user=postgres password=pass")

cursor=conn.cursor()

#fetch mr data from database
mr = '''select MR from users where uid=1'''

#run brainsuite to get skull-stripped mr data
import os

#os.system(path of cortical_extraction.sh space path of mr data file)
os.system("/Applications/BrainSuite18a/bin/cortical_extraction.sh /path/gfilename.nii")
#output file same path as filename.nii

#upload skull-stripped mr data to database - subject 1 and 2
#subject 1 and 2 both use the standard brain
cursor.excute('''insert into users where uid=1 value
              (,,,,/path/filename_cerebrum_mask.nii.gz)''')

cursor.excute('''insert into users where uid=2 value
              (,,,,/path/filename_cerebrum_mask.nii.gz)''')