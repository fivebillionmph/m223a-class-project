#Course Name: BE 223A 18Fall 
#Author Name: Yannan Lin
#Purpose: Skull-stripping through BrainSuite

#run brainsuite to get skull-stripped mr data
import os

#os.system(path of cortical_extraction.sh space path of mr data file)
os.system("/Applications/BrainSuite18a/bin/cortical_extraction.sh /Users/yannanlin/Desktop/T1.nii.gz")

#output file same path as filename.nii

