# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage
import nibabel as nib

from traits.api import HasTraits, Range, Instance, on_trait_change, Button
from traitsui.api import View, Item, Group, VGroup, HGroup

from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, SceneEditor, MlabSceneModel

import pandas as pd


NO_READIN = 0
YES_READIN = 1
    
SOURCE_IS_EEG = 0
SOURCE_IS_ECOG = 1
ELECTRODE_OFF = 0
ELECTRODE_ON = 1

def createMask(brain):
    row,col,depth = brain.shape
    mask = np.zeros([row,col,depth])
    for i in range(row):
        for j in range(col):
            for k in range(depth):
                if brain[i,j,k] > 0:
                    mask[i,j,k]=1
                else:
                    mask[i,j,k]=0                    
    return mask

def calcVolume(mask):
    vol = 0
    fMask = mask.flatten()
    for voxel in fMask:
        if voxel > 0:
            vol+=1
    return vol

def diluteMask(mask):
    volOri = calcVolume(mask)
    dMask = ndimage.gaussian_filter(mask,1)
    dMask = createMask(dMask)
    volDilute = calcVolume(dMask)
    return dMask,volOri,volDilute

def askUserForMethod(cursor, subject_id):
    cursor.execute("select distinct method from scores where sid = %s", (subject_id, ))
    methods = [x["method"] for x in cursor.fetchall()]
    while True:
        for i in range(len(methods)):
            print("%d: %s" % (i, methods[i]))
        user_choice = input("Select a method or q to quit ")
        if user_choice == "q":
            return False
        try:
            uci = int(user_choice)
            method = methods[uci]
            return method
        except:
            print("Invalid choice")

def readScore(cursor, subject_id, method):
    # For database table
    # return score(2d numpy array, m channel X n time), channel num, timestep num

    #######
    # transform score into 2d numpy here
    # score
    #######
    
    #scoreNorm = [s/(score.max)*50000 for s in score] #Normalize the score

    #return scoreNorm,scoreNorm.shape
    cursor.execute("select * from scores where sid = %s and method = %s", (subject_id, method))
    scores = cursor.fetchall()
    greatest_score_index = None
    for i in range(100):
        if scores[0]["score" + str(i)] is None:
            break
        greatest_score_index = i
    scores_array = np.zeros(shape=(len(scores), greatest_score_index + 1))
    for i in range(len(scores)):
        row = scores[i]
        for j in range(greatest_score_index + 1):
            scores_array[i][j] = row["score" + str(j)]
    #scoreNorm = [s/(scores_array.max)*50000 for s in scores_array] #Normalize the score
    scoreNorm = (scores_array / scores_array.max()) * 50000 #Normalize the score
    return scoreNorm, len(scores), greatest_score_index + 1

def readPos(cursor, subject_id):
    # For database table 
    # return 1d list x,y and z

    # return x,y,z
    cursor.execute("select * from channels where sid = %s", (subject_id, ))
    channels = cursor.fetchall()
    x = [c["x"] for c in channels]
    y = [c["y"] for c in channels]
    z = [c["z"] for c in channels]
    return x,y,z

def getSkullStrippedBrainFile(cursor, subject_id):
    cursor.execute("select mr_path from subjects where sid = %s", (subject_id,))
    return cursor.fetchone()["mr_path"] # file of brain

def locateElectron(space3d,score1d,X,Y,Z):
    # space3d: 3d numpy array
    # score1d: 1d numpy array
    # X,Y,Z: 1d list
    N = len(X)  
    for i in range(0,N):
        space3d[X[i],Y[i],Z[i]] = score1d[i]

    return space3d

def convolutionHeatmap(timestep,row,col,depth,score2d,X,Y,Z,mask):
    # score2d: 2d numpy array, m channel X n time
   
    heatmap = np.zeros([timestep,row,col,depth])
    for t in range(timestep):
        blankSpace = np.zeros([row,col,depth])
        electrodeSpace = locateElectron(blankSpace, score2d[:,t], X, Y, Z)
        convSpace = ndimage.gaussian_filter(electrodeSpace,5)
        heatmap[t] = convSpace * mask

    return heatmap

class HeatMap:
    def __init__(self, cursor, subject_id, scoring_method):
        mriBrainMask = getSkullStrippedBrainFile(cursor, subject_id)
        brain = nib.load(mriBrainMask)
        self.brainMask = createMask(brain.get_fdata())
        self.brainDMask, volOri, volDilute = diluteMask(self.brainMask)
        self.row, self.col, self.depth = self.brainMask.shape
        print('MRI brain mask loaded successfully')

        self.POS_FLAG = NO_READIN
        self.SCORE_FLAG = NO_READIN

        # PosX is a m channel list
        self.PosX, self.PosY, self.PosZ = readPos(cursor, subject_id)
        self.POS_FLAG = YES_READIN
        print('Load Electrodes positions successfully')

        # score is m channel x n time numpy array
        self.Score, self.ChannelNum, self.timestep = readScore(cursor, subject_id, scoring_method)
        self.SCORE_FLAG = YES_READIN
        print('Load Scores successfully')

    def generateHeatmap(self):
        if not (self.POS_FLAG and self.SCORE_FLAG):
            print('Requiring data missing. Flag:  ', self.POS_FLAG, self.SCORE_FLAG)
        else:
            self.Heatmap = convolutionHeatmap(self.timestep, self.row, self.col, self.depth, self.Score, self.PosX, self.PosY, self.PosZ, self.brainDMask)
            self.HeatmapVmax = self.Heatmap.max()
            self.HeatmapVmin = self.Heatmap.min()

            self.HEATMAP_FLAG = YES_READIN

            print('Heatmap generation finished')

    def show(self):
        if not self.HEATMAP_FLAG:
            print('Requiring heatmap not generated')
        else:
            my_model = MyModel(self.brainMask,self.Heatmap,self.PosX,self.PosY,self.PosZ,self.HeatmapVmin,self.HeatmapVmax,self.timestep)
            my_model.configure_traits()
        

class MyModel(HasTraits):
    scene = Instance(MlabSceneModel,())
    plot = Instance(PipelineBase)
    
    signalType = Button('No Use')
    electrodesType = Button('On/Off Electrodes')
    time = Range(0,100,0)  # Because we have no time series currently, so I directly set the time as one time step

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=700, width=800, show_label=False),
                VGroup(
                        '_', Item(name='time'),'_', 
                        HGroup(
                            Item(name = 'signalType', label= 'No Use',show_label=True),
                            Item(name = 'electrodesType', label = 'Electrodes',show_label=True)
                            ),
                        show_border=True
                        
                        ),
                resizable=True
                )



    def __init__(self,brainMask,heatmap,posx,posy,posz,vmin,vmax,timeBoundary):
        HasTraits.__init__(self)
        self.brain = brainMask
        self.Heatmap = heatmap

        self.posx = posx
        self.posy = posy
        self.posz = posz

        self.vmin = vmin
        self.vmax = vmax

        self.timeBoundary = timeBoundary

        self.electrode = ELECTRODE_OFF



    @on_trait_change('time,scene.activated')
    def update_time(self):
        if self.time < self.timeBoundary:
            heatmap = self.Heatmap[self.time]
        else:
            heatmap = self.Heatmap[self.timeBoundary-1]

        if self.plot is None:
            background = self.scene.mlab.pipeline.scalar_field(self.brain)
            self.scene.mlab.pipeline.iso_surface(background,vmin=0,vmax=1,opacity=1.0,colormap='gray',figure=self.scene.mayavi_scene)

            heat = self.scene.mlab.pipeline.scalar_field(heatmap)
            self.plot = self.scene.mlab.pipeline.volume(heat,vmax=self.vmin + .8*(self.vmax-self.vmin), vmin=self.vmin,figure=self.scene.mayavi_scene)
                
            self.scene.mlab.view(azimuth=180,elevation=80,distance=350)
        else:
            self.plot.mlab_source.scalars = heatmap

    @on_trait_change('electrodesType') # switch electrodes visuliaztion on and off.
    def update_points(self):
        electronX = self.posx
        electronY = self.posy
        electronZ = self.posz
               
        if self.electrode == ELECTRODE_OFF:
            self.electrode = ELECTRODE_ON

            # replace this function with Yen's better colored version of channel plotting. noted by Aaron 11/11/2018
            self.elec = self.scene.mlab.points3d(electronX, electronY, electronZ, scale_factor=10, resolution=20, scale_mode='none', color = (1,0,1), opacity = 1.0, figure=self.scene.mayavi_scene)
            #############################################################################

            self.scene.mlab.view(azimuth=180,elevation=80,distance=350)
        else:
            self.electrode = ELECTRODE_OFF
            self.elec.stop()           


    @on_trait_change('signalType') # change heatmap between EEG and ECoG... not anymore
    def update_source(self):
        pass

    
def run(cursor, subject_id):
    while True:
        scoring_method = askUserForMethod(cursor, subject_id)
        if not scoring_method:
            return
        Test = HeatMap(cursor, subject_id, scoring_method)
        Test.generateHeatmap()
        Test.show()
    
