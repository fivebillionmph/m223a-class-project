#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 22:51:55 2018

@author: yannanlin
"""

import psycopg2
import nibabel as nib
import math

#connect to database
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn=psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor()


#pull coordiante data from database - channel table
########TO DO######
#format [[x1,y1,z1],[x2,y2,z2]]
electrode_coord_list = []

#pull MR data from database - subject table
########TO DO######
x,y,z = mr_brain_mask_data.shape

#find coordinates of all the points that make up the brain mask
#return a list of coordinates
coord_list = []
for x in range(160):
    for y in range(256):
        for z in range(256):
            if mr_brain_mask_data[x,y,z] > 0:
                coord_list.append([x,y,z])

class ChannelCorrection(object):
    '''
    Function to correct the coordinates of the floating electrodes, if any.
    For an ECoG subject, MR data needs to be passed in.
    
    PointDistance function calculates the distance between the electrode and 
    every point on the surface mask.
    
    CoordCorrection works to 
    1 calculate all the distances between the 
    elecrtrode and every point on the surface mask, 
    2 find the nearest point 
    that renders the shorest distance between the electrode and the point on 
    the surface mask, 
    3 compare the shorest distance to a threshold value, 
    4 if the shorest distance is greater than the threshold value, the 
    coordinates of the electrode will be corrected by using the coordinates
    of the point on the surface mask instead.
    
    Threshold value 6.71 is based on the largest distance of the 63 EEG 
    electrodes and only works for mlab.point3d(x,y,z, scale_factor=10).
    If scale_factor changes, the threshold value will need to be adjusted 
    accordingly.
    
    '''
    def __init__(self, mr_data):
        self.mr_data = mr_data
        
    def get_mr_data(self):
        return self.mr_data
 
    #calculate distance between two 3d points
    def PointDistance(self,x1, y1, z1, x2, y2, z2):  
        point_dis = math.sqrt(math.pow(x2 - x1, 2) +
                    math.pow(y2 - y1, 2) +
                    math.pow(z2 - z1, 2)* 1.0) 
        return point_dis
    
    #find the coords of the point that gives the shortest distance
    def CoordCorrection(self):
        min_list = []
        for a in range(len(electrode_coord_list)):
            min_dist = 100000 #reset min_dist to 100000
            for i in range(len(coord_list)):
                dis = self.PointDistance(coord_list[i][0], 
                                          coord_list[i][1], 
                                          coord_list[i][2], 
                                          electrode_coord_list[a][0],
                                          electrode_coord_list[a][1],
                                          electrode_coord_list[a][2])
                if dis < min_dist:
                    min_dist = dis
                    min_list = []
                    min_list.append([coord_list[i][0], coord_list[i][1], coord_list[i][2]])
                    
            if min_dist > 6.71:
                electrode_coord_list[a] = min_list[0]
            #may comment out the print function later
            print(electrode_coord_list[a])
        return electrode_coord_list #format [[x1,y1,z1],[x2,y2,z2]]
    
#upload corrected coordiante list to database
########TO DO######
        
    
    
    

##################Test: Using EEG subject and coordinates####################
        
##################Fist, run the following code################################
#MR data       
mr_brain_mask = nib.load('/Users/yannanlin/Desktop/homework/BE 223A/BE223A data/Standard_Brain/standard.cerebrum.mask.nii.gz')
mr_brain_mask_data = mr_brain_mask.get_fdata()
#EEG electrodes
electrode_coord_list = [[61, 200, 189], [81, 201, 185], [103, 200, 190], 
                        [40, 188, 190], [56, 190, 200], [80, 190, 205], 
                        [105, 190, 202], [123, 189, 193], [27, 173, 188], 
                        [40, 173, 201], [52, 173, 205], [65, 173, 212], 
                        [80, 173, 218], [125, 172, 204], [109, 173, 212], 
                        [95, 173, 216], [138, 173, 190], [19, 148, 180], 
                        [25, 148, 200], [38, 148, 213], [56, 148, 220], 
                        [79, 148, 227], [100, 148, 225], [122, 148, 219], 
                        [140, 148, 203], [150, 148, 180], [153, 122, 167], 
                        [149, 122, 194], [131, 122, 216], [103, 122, 226], 
                        [78, 122, 230], [52, 122, 222], [32, 122, 207], 
                        [18, 122, 192], [12, 122, 173], [10, 92, 170], 
                        [18, 92, 195], [32, 92, 210], [52, 92, 221], 
                        [78, 92, 230], [103, 92, 225], [129, 92, 215], 
                        [147, 90, 193], [153, 90, 165], [20, 65, 174], 
                        [26, 65, 192], [40, 65, 202], [54, 64, 213], 
                        [78, 65, 218], [101, 65, 215], [118, 65, 205], 
                        [135, 63, 189], [137, 63, 170], [36, 45, 176], 
                        [50, 50, 191], [78, 45, 200], [106, 49, 192], 
                        [117, 47, 175], [58, 40, 178], [78, 35, 180], 
                        [98, 40, 178], [78, 32, 160], [81, 210, 170]]

####################Next, run from line x,y,z = mr_brain_mask_data.shape to end of the ChannelCorrection class

###################Last, run the following code################################
brain = ChannelCorrection(mr_brain_mask_data)
print(brain.CoordCorrection())

#################Expected output same as electrode_coord_list##################
#[[61, 200, 189], [81, 201, 185], [103, 200, 190], [40, 188, 190], [56, 190, 200], 
# [80, 190, 205], [105, 190, 202], [123, 189, 193], [27, 173, 188], [40, 173, 201], 
# [52, 173, 205], [65, 173, 212], [80, 173, 218], [125, 172, 204], [109, 173, 212], 
# [95, 173, 216], [138, 173, 190], [19, 148, 180], [25, 148, 200], [38, 148, 213], 
# [56, 148, 220], [79, 148, 227], [100, 148, 225], [122, 148, 219], [140, 148, 203], 
# [150, 148, 180], [153, 122, 167], [149, 122, 194], [131, 122, 216], [103, 122, 226], 
# [78, 122, 230], [52, 122, 222], [32, 122, 207], [18, 122, 192], [12, 122, 173], 
# [10, 92, 170], [18, 92, 195], [32, 92, 210], [52, 92, 221], [78, 92, 230], 
# [103, 92, 225], [129, 92, 215], [147, 90, 193], [153, 90, 165], [20, 65, 174], 
# [26, 65, 192], [40, 65, 202], [54, 64, 213], [78, 65, 218], [101, 65, 215], 
# [118, 65, 205], [135, 63, 189], [137, 63, 170], [36, 45, 176], [50, 50, 191], 
# [78, 45, 200], [106, 49, 192], [117, 47, 175], [58, 40, 178], [78, 35, 180], 
# [98, 40, 178], [78, 32, 160], [81, 210, 170]]

