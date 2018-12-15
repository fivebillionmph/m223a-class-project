'''
SIGNAL ANALYSIS: Power Analysis (Jake "method 3")
'''

import os

def run(cursor, filename, startTime, stopTime, interval, startFrequency, stopFrequency):
    os.system("power_analysis\\Power_Analysis_2.exe" + " " + filename + " " + startTime + " " + stopTime + " " +
              interval + " " + startFrequency + " " + stopFrequency)
    #new_file = re.sub(r"(.*).([^.]*)$", r"\1.csv", (filename))
    #with open(new_file, "r") as f:
    #    csvreader = csv.reader(f)
    #    row = next(csvreader)
        
