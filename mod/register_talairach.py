# -*- coding: utf-8 -*-
"""
Talairach electrode localization/registration (Joseph Tseung)

Created on Wed Nov 14 00:04:29 2018

@author: josep
"""

""" Talairach coordinate to MRI visualization """

# read Talairach coordinates from CSV into a list called Temp
import csv
import .util
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os

# import nibabel as nib
# from mayavi import mlab
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename
# 
# Tk().withdraw()

def run(cursor, subject_id):
    file = util.inputFilepath("Select Talairach coordinates file ")
    
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
    file_dir = os.path.dirname(os.path.realpath(file))
    with open(os.path.join(file_dir, 'talairach_coordinates.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(x)):
            writer.writerow([x[i], y[i], z[i]])
    print("Done writing Talairach coordinates csv.")
    
    # Batch convert Talairach to MNI coordinates mni2tal from Yale
    # "TAL -> MNI Batch Convert"
    # Output is in file 'converted.csv' and in columns E,F,G
    
    driver = webdriver.Chrome('C:\\Users\\josep\\Python\\chromedriver.exe')
    driver.get("http://www.google.com/")
    
    #open tab
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
    
    # Load a page 
    driver.get('https://bioimagesuiteweb.github.io/webapp/mni2tal')
    
    # Tab through
    for i in range(16):
        driver.find_element_by_tag_name('body').send_keys(Keys.TAB)
    driver.find_element_by_tag_name('body').send_keys(u'\ue007')
    
    # click button
    python_button = driver.find_element_by_id('batch2')
    python_button.click()
     
    # type text
    elm = driver.find_element_by_xpath("//input[@type='file']")
    elm.send_keys(os.getcwd() + "\\talairach_coordinates.csv")
    
    # close the tab
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w') 
    driver.close()
    
    # Read-in MNI coordinates now
    # from tkinter import Tk
    # from tkinter.filedialog import askopenfilename
    # 
    # Tk().withdraw()
    file = util.inputFilepath("Select MNI coordinates file ")
    
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
    
    
    # from tkinter import Tk
    # from tkinter.filedialog import askopenfilename
    
    # Use MNI atlas to do visualization
    # Tk().withdraw()
    file = util.inputFilepath("Select MNI Template ")
    
    # fix-up points
    temp = np.column_stack((x,y,z))
    
    # rotate yz plane counterclockwise 45 degrees
    yz_temp = temp[:,[1,2]]
    theta = np.radians(45)
    c,s = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array([[c,s], [-s,c]])
    yz_temp = np.dot(yz_temp, rotation_matrix)
    temp[:,[1,2]] = yz_temp
    
    
    temp[:,0] += 70
    temp[:,1] += 140
    temp[:,2] += 90

    results = []
    for i in range(len(rotated)):
        results.append({"x": temp[:, 0][i], "y": temp[:, 1][i], "z": temp[:, 2][i]})

    return results
