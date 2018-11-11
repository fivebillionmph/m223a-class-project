#Course Name: BE 223A 18Fall 
#Author Name: Yannan Lin
#Purpose: ECoG Channel Plotting

#connect to database
import psycopg2

conn = psycopg2.connect("user=postgres password=pass")

cursor=conn.cursor()

####################ECoG Channel Plotting#####################
import nibabel as nib
from mayavi import mlab

#fetch data from database
smr = '''select filename.nii.gz from users where uid=3'''

#load mr brain mask data - pt brain
mr_head = nib.load(smr)
mr_head_data = mr_head.get_fdata()

#create mayavi scene
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))

#display mr data
source_2 = mlab.pipeline.scalar_field(mr_head_data)

#contour surface
surface = mlab.pipeline.iso_surface(source_2, 
                          contours=[100,], 
                          opacity=1, 
                          colormap = 'black-white')

#fetch coordinate data from database and plot on cortex
cursor.excute('select * from ECoGtable')

all_coor = cursor.fetchall()

for i in all_coor:
    mlab.points3d(i[1], i[2], i[3], color=(0, 1, 0), scale_factor=10)

mlab.show()
mlab.show()

