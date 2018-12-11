# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:01:04 2018

@author: josep
"""
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename
import SimpleITK as sitk
# from skimage import measure
from matplotlib import pyplot as plt

# Tk().withdraw()
# filename = askopenfilename(title = "Select registered image")
image = sitk.ReadImage(filename)

# fix up some image characteristics
image.SetOrigin((0,0,0))
image.SetDirection([1,0,0,0,1,0,0,0,1])
image.SetSpacing([1,1,1])


# Cast/normalize to an image with a 0-255 range
image_255 = sitk.Cast(sitk.RescaleIntensity(image), sitk.sitkUInt8)

# Get information on image intensity distribution
intensities = []

for i in range(image.GetWidth()):
  for j in range(image.GetHeight()):
    for k in range(image.GetDepth()):
        intensities.append(image_255.GetPixel(i,j,k))
        
fig = plt.figure()
plt.title('Intensity Histogram')
plt.xlabel("Pixel intensity")
plt.ylabel("Number of pixels")
plt.hist(intensities)
plt.show()
print("Done getting intensities")

# Hard-coded threshold based on intensity histogram results
thresholded_image = image_255 > 250

# Gaussian blurring to take out high-resolution noise
gaussian = sitk.SmoothingRecursiveGaussianImageFilter()
gaussian_blurred = gaussian.Execute(thresholded_image)
# Cast/normalize to an image with a 0-255 range
gaussian_blurred_255 = sitk.Cast(sitk.RescaleIntensity(gaussian_blurred), sitk.sitkUInt8)
print("Done blurring")

# Display connected component sizes
stats = sitk.LabelShapeStatisticsImageFilter()
stats.Execute(sitk.ConnectedComponent(gaussian_blurred_255))
    
label_sizes = [stats.GetNumberOfPixels(l) for l in stats.GetLabels()]

plt.hist(label_sizes)
plt.title("Distribution of Object Sizes")
plt.xlabel("Size in Pixels")
plt.ylabel("Number of Objects")

# output electrode locations s tuples
electrodes = []
for l in stats.GetLabels():
    if (100 < stats.GetNumberOfPixels(l) < 1000):
        electrodes.append(stats.GetCentroid(l))
n = len(electrodes)
print(str(n) + " electrodes found")

# modify electrode coordinates here:
x = []
y = []
z = []

# first switch x and z axes to convert from SimpleITK format to numpy array format
for i in range(len(electrodes)):
    x.append(float(electrodes[i][2]))
    y.append(float(electrodes[i][1]))
    z.append(float(electrodes[i][0]))

import numpy as np
attempt = np.column_stack([x,y,z])

# rotate by 90 degrees towards the xy plane and 45 degrees towards yz plane
theta = np.radians(90)
c,s = np.cos(theta), np.sin(theta)
rotation_matrix = np.array([[c,0,s], [0,1,0], [-s, 0, c]])
rotated = np.dot(attempt, rotation_matrix)

"""
# rotate yz plane clockwise 45 degrees
yz_tempt = rotated[:,[1,2]]
theta = np.radians(45)
c,s = np.cos(theta), np.sin(theta)
rotation_matrix = np.array([[c,-s], [s,c]])
yz_rotated = np.dot(yz_tempt, rotation_matrix)
rotated[:,[1,2]] = yz_rotated
"""

rotated[:, 0] += image.GetWidth()/2

# save electrode locations in csv format
import csv
with open('electrode_coordinates.csv', mode='w', newline='') as electrode_coordinates:
    writer = csv.writer(electrode_coordinates)
    writer.writerows(rotated)
print('csv done')
