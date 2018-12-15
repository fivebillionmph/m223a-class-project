#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Electrode Position Correction (Yannan Lin)

Created on Tue Nov 27 22:51:55 2018

@author: yannanlin
"""

import nibabel as nib
import pandas as pd
import math

def run(cursor, subject_id, smr_path, coord_data):

    #####################################################################
    ###################Grab Data from Database###########################
    #####################################################################

    # get original x, y, z
    x = []
    y = []
    z = []
    for i in range(len(coord_data)):
        x.append(coord_data[i]["x"])
        y.append(coord_data[i]["y"])
        z.append(coord_data[i]["z"])

    # format coordinates to a list of [x1,y1,z1]
    electrode_coord_list = []
    for a in range(len(x)):
        electrode_coord_list.append([x[a],y[a],z[a]])

    # get SMR data from database - subject table
    #####TO DO#####
    mr_brain_mask = nib.load(smr_path)
    mr_brain_mask_data = mr_brain_mask.get_fdata()
    x,y,z = mr_brain_mask_data.shape

    #####################################################################
    ###################Channel Correction################################
    #####################################################################

    # find coordinates of all the points that make up the brain mask
    coord_list = []
    for x in range(mr_brain_mask_data.shape[0]):
        for y in range(mr_brain_mask_data.shape[1]):
            for z in range(mr_brain_mask_data.shape[2]):
                if mr_brain_mask_data[x,y,z] > 0:
                    coord_list.append([x,y,z])

    # function to correct the coordinates of the floating electrodes
    class ChannelCorrection(object):
        '''
        Function to correct the coordinates of the floating electrodes, if any.
        For an ECoG subject, skull-stripped MR data needs to be passed in. This
        is a conditional function, it will modify the coordinates under the
        condition that less than 5% of the total electrodes are off of the
        cortical surface, meaning 5% of them are not sitting on the surface.
        
        PointDistance function calculates the distance between the electrode and
        every point on the surface mask.
        
        CoordCorrection works to
        1 calculate all the distances between the
        electrode and every point on the surface mask,
        2 find the nearest point that renders the shortest distance between
        the electrode and the point on the surface mask,
        3 calculate the distance between the nearest point on surface and the electrode,
        4 calculate the proportion of the distance from the electrode to the
        nearest point on surface that is greater than 6.71 (a pre-defined threshold
        value), if the proportion is less than 0.05, then replace the original
        electrode coordinates with the coordinates of the nearest point on surface
        
        Note:
        Threshold value 6.71 is based on the largest distance of the 63 EEG
        electrodes and only works for mlab.point3d(x,y,z, scale_factor=10).
        If scale_factor changes, the threshold value will need to be adjusted
        accordingly. If the distance from the electrode to the nearest point
        on surface is greater than 6.71, it looks like floating around or
        inside the surface rather than sitting on it.
        
        Input and output data format: [[x1,y1,z1],[x2,y2,z2]...]
        
        '''
        def __init__(self, mr_data):
            self.mr_data = mr_data
        
        def get_mr_data(self):
            return self.mr_data
     
        # calculate distance between two 3d points
        def PointDistance(self,x1, y1, z1, x2, y2, z2):
            point_dis = math.sqrt(math.pow(x2 - x1, 2) +
                        math.pow(y2 - y1, 2) +
                        math.pow(z2 - z1, 2)* 1.0)
            return point_dis
        
        #find the coords of the point that gives the shortest distance
        def coord_correction(self):
            min_list = [] #coordiantes of the nearest point on surface to each electrode
            min_coord_list = [] #list of coordiantes of nearest points for each elecrode
            min_dist_list = [] #list of distances between every nearest point and electrode
            count = 0
        
            for a in range(len(electrode_coord_list)):
                min_dist = 100000 #reset min_dist to 100000
                for i in range(len(coord_list)):
                    dis = self.PointDistance(coord_list[i][0],
                                              coord_list[i][1],
                                              coord_list[i][2],
                                              electrode_coord_list[a][0],
                                              electrode_coord_list[a][1],
                                              electrode_coord_list[a][2])
                    
                    #get the coordiante of the nearest point on the surface to each electrode
                    if dis < min_dist:
                        min_dist = dis
                        min_list = [coord_list[i][0], coord_list[i][1], coord_list[i][2]]
                        
                min_coord_list.append(min_list)
                min_dist_list.append(min_dist)
                
                #6.71 is the threshold found from 63 EEG channels
                if min_dist > 6.71:
                    count += 1
                    
            #calculate the proportion of points that are 6.71 unitss off of the surface
            proportion = count/len(electrode_coord_list)
            
            #only correct the coordiantes if <5% of them are 6.71 units off of the surface
            if proportion < 0.05:
                for i in range(len(electrode_coord_list)):
                    if min_dist_list[i] > 6.71:
                        electrode_coord_list[i] = min_coord_list[i]
                        
            return electrode_coord_list #format [[x1,y1,z1],[x2,y2,z2]]

    # create an object
    brain = ChannelCorrection(mr_brain_mask_data)
    electrode_coord_list_update = brain.coord_correction()

    # change format of coordinates before updating database
    x_new = []
    y_new = []
    z_new = []

    for i in range(len(electrode_coord_list_update)):
        x_new.append(electrode_coord_list_update[i][0])
        y_new.append(electrode_coord_list_update[i][1])
        z_new.append(electrode_coord_list_update[i][2])
    
    update_coord = pd.DataFrame(
                                {'x_new': x_new,
                                'y_new': y_new,
                                'z_new': z_new
                                })
    
    #####################################################################
    ###################Update Database###################################
    #####################################################################

    update_channels = "insert into channels (x, y, z, sid) values(%s, %s, %s, %s);"

    for i in range(len(update_coord)):
        cursor.execute(update_channels, (int(update_coord.iloc[:,0][i]),
                                         int(update_coord.iloc[:,1][i]),
                                         int(update_coord.iloc[:,2][i]), subject_id))
