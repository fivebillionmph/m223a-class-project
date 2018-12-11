# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 00:04:29 2018

@author: josep
"""

""" Talairach coordinate to MRI visualization """

# read Talairach coordinates from CSV into a list called Temp
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
file = askopenfilename(title = "Select Talairach coordinates file")

temp = []    
x = []
y = []
z = []

with open(file, 'r') as coordinates:
    reader = csv.reader(coordinates, delimiter='\t')
    # skips the header
    next(coordinates)
    for row in reader:
        temp.append(row)
print("Done reading CSV file.")

# iterate through temp to get the Talairach coordinates
for i in range(len(temp)-1):
    x.append(float(temp[i][1]))
    y.append(float(temp[i][2]))
    z.append(float(temp[i][3]))
print("Done getting Talairach coordinates")

# write to CSV file containing only the 3 columns
with open('talairach_coordinates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(len(x)):
        writer.writerow([x[i], y[i], z[i]])
print("Done writing Talairach coordinates csv.")

# Batch convert Talairach to MNI coordinates using this app: http://sprout022.sprout.yale.edu/mni2tal/mni2tal.html
# "TAL -> MNI Batch Convert"
# Output is in file 'converted.csv' and in columns E,F,G

# Read-in MNI coordinates now
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
file = askopenfilename(title = "Select MNI coordinates file")

temp = []    
x = []
y = []
z = []

with open(file, 'r') as coordinates:
    reader = csv.reader(coordinates)
    # skips the header
    next(coordinates)
    for row in reader:
        temp.append(row)
print("Done reading CSV file.")

for i in range(len(temp)):
    x.append(float(temp[i][4]))
    y.append(float(temp[i][5]))
    z.append(float(temp[i][6]))
print("Done getting MNI coordinates")

# Use MNI atlas to do visualization
# Before visualizing with Mayavi (which uses numpy arrays), need to switch x and z coordinates
