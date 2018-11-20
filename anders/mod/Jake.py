#Power Analysis

import os
import re
import csv

def run(cursor, filename, startTime, stopTime, startFrequency, stopFrequency):
    os.system("..\\Jake\\Power_Analysis.exe" + " " + filename + " " + startTime + " " + stopTime + " " + startFrequency + " " + stopFrequency)
    #new_file = re.sub(r"(.*).([^.]*)$", r"\1.csv", (filename))
    #with open(new_file, "r") as f:
    #    csvreader = csv.reader(f)
    #    row = next(csvreader)
        
