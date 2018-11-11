#Course Name: BE 223A 18Fall
#Author Name: Yannan Lin
#Purpose: EEG 10X20 Channel Plotting

#connect to database
import psycopg2

conn = psycopg2.connect("user=postgres password=pass")

cursor=conn.cursor()

###################EEG Channel Plotting##################
import nibabel as nib
from mayavi import mlab
import xlrd

#load mr brain mask data - standard brain
smr = '''select filename.nii.gz from users where uid=1'''
mr_brain_mask = nib.load(smr)
mr_brain_mask_data = mr_brain_mask.get_fdata()

#create mayavi scene
fig = mlab.figure(bgcolor=(1, 1, 1), size=(500, 500))

#display mr data
source = mlab.pipeline.scalar_field(mr_brain_mask_data)


#contour surface
surface = mlab.pipeline.iso_surface(source, 
                          contours=[100,], 
                          opacity=1, 
                          colormap = 'black-white')

#load coordinate data spreadsheet to python
loc = '/Users/yannanlin/Desktop/homework/BE 223A/BE223A data/EEG_10X20.xlsx'
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

#upload coordinate data to database
a = 1
while a < 64:
    coor = '''insert into EEGtable(EEG Name, X, Y, Z) values
                 (sheet.cell_value(a,0),
                  sheet.cell_value(a,1),
                  sheet.cell_value(a,2),
                  sheet.cell_value(a,3))'''
    a += 1
    
cursor.excute(coor)

#get coordinate data from database and plot on cortex
cursor.excute('select * from EEGtable')

all_coor = cursor.fetchall()

for i in all_coor:
    mlab.points3d(i[1], i[2], i[3], color=(0, 1, 0), scale_factor=10)

mlab.show()





