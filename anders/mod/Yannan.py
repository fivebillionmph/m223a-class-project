#Course Name: BE 223A 18Fall 
#Author Name: Yannan Lin
#Purpose: Skull-stripping through BrainSuite

#run brainsuite through command line
import os

def run(cursor, subject_id, brain_suite_path, nii_file):
    os.system(brain_suite_path + " " + nii_file)
    #new_file = nii_file
    #cursor.execute("update subjects set smr_path = %s where sid = %s", ())

# #For MAC
# os.system("/Applications/BrainSuite18a/bin/cortical_extraction.sh /Users/yannanlin/Desktop/T1.nii.gz")
# 
# #For Windows
# os.system(r'''"C:\Program Files\BrainSuite18a\bin\cortical_extraction.cmd" C:\Users\aa\Desktop\T1.nii.gz''')


#output skull-stripped mr data file has the same path as filename.nii.gz
