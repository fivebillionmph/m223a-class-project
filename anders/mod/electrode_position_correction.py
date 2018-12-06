#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 22:51:55 2018

@author: yannanlin
"""

import nibabel as nib
import pandas as pd
import math

def run(cursor, subject_id, smr_path):

    #####################################################################
    ###################Grab Data from Database###########################
    #####################################################################

    # get coordiante data from database - channel table
    cursor.execute("""select * from channels where sid = %s""", (subject_id, ))
    coord_data = cursor.fetchall()

    # get channel
    channel = []
    for i in range(len(coord_data)):
        channel.append(coord_data[i][1])

    # get original x, y, z
    x = []
    y = []
    z = []
    for i in range(len(coord_data)):
        x.append(coord_data[i][3])
        y.append(coord_data[i][4])
        z.append(coord_data[i][5])

    # format coordinates to a list of [x1,y1,z1]
    electrode_coord_list = []
    for a in range(len(x)):
        electrode_coord_list.append([x[a],y[a],z[a]])

    # get SMR data from database - subject table
    #####TO DO#####
    mr_brain_mask = nib.load(smr_path) ## find the skull-stripped mr data??????
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
        For an ECoG subject, skull-stripped MR data needs to be passed in.
        
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
        
        # find the coords of the point that gives the shortest distance
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
                # print(electrode_coord_list[a])
            return electrode_coord_list #format [[x1,y1,z1],[x2,y2,z2]]

    # create an object
    brain = ChannelCorrection(mr_brain_mask_data)
    electrode_coord_list_update = brain.CoordCorrection()

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

    update_channels = "UPDATE channels set x=%s, y=%s, z=%s WHERE sid = %s;"

    for i in range(len(update_coord)):
        cursor.execute(update_channels, (int(update_coord.iloc[:,0][i]),
                                         int(update_coord.iloc[:,1][i]),
                                         int(update_coord.iloc[:,2][i]), subject_id))
