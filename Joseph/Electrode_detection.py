# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:01:04 2018

@author: josep
"""
# Call a GUI for user to select image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import SimpleITK as sitk
# from skimage import measure
from matplotlib import pyplot as plt

Tk().withdraw()
filename = askopenfilename(title = "Select registered image")
image = sitk.ReadImage(filename)

"""
# fix up some image characteristics
image.SetOrigin((0,0,0))
image.SetDirection([1,0,0,0,1,0,0,0,1])
image.SetSpacing([1,1,1])
"""

# Cast/normalize to an image with a 0-255 range
image_255 = sitk.Cast(sitk.RescaleIntensity(image), sitk.sitkUInt8)

"""
# Can try using sitk.LabelIntensityStatisticsImageFilter() to get intensity_stats
intensity = sitk.LabelIntensityStatisticsImageFilter()
intensity.Execute(image_255()
    
intensity_stats = [intensity(l) for l in stats.GetLabels() if l != 1]

# Try iterating through the loop and displaying histogram data
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
"""

# Hard-coded threshold based on intensity histogram results
thresholded_image = image_255 > 250
# sitk.WriteImage(thresholded_image, 'thresholded_image'+'.nii.gz')

# Try a different kind of Gaussian blurring
gaussian = sitk.SmoothingRecursiveGaussianImageFilter()
gaussian_blurred = gaussian.Execute(thresholded_image)
# Cast/normalize to an image with a 0-255 range
gaussian_blurred_255 = sitk.Cast(sitk.RescaleIntensity(gaussian_blurred), sitk.sitkUInt8)
# sitk.WriteImage(gaussian_blurred, 'gaussian_blurred_image' + '.nii.gz')
print("done blurring")

# Display connected component sizes
stats = sitk.LabelShapeStatisticsImageFilter()
stats.Execute(sitk.ConnectedComponent(gaussian_blurred_255))
    
label_sizes = [stats.GetNumberOfPixels(l) for l in stats.GetLabels()]

plt.hist(label_sizes)
plt.title("Distribution of Object Sizes")
plt.xlabel("Size in Pixels")
plt.ylabel("Number of Objects")

# output electrode locations
# 91 fell in the range of 200-400
# 116 fell in the range of 100-1000
# looked off when Yannan plotted in mayavi
electrodes = []
for l in stats.GetLabels():
    if (100 < stats.GetNumberOfPixels(l) < 1000):
        electrodes.append(stats.GetCentroid(l))
print(len(electrodes)) 

# Direction cosine matrix as a 1D array in row-major form
# Origin in physical space
# Physical size of each pixel
print(gaussian_blurred_255.GetDirection())
print(gaussian_blurred_255.GetOrigin())
print(gaussian_blurred_255.GetSpacing())
print("Done getting Direction, Origin, & Spacing.")

# save electrode locations in csv format
import csv
with open('electrode_coordinates_after_fixing_origin_and_direction.csv', mode='w', newline='') as electrode_coordinates:
    writer = csv.writer(electrode_coordinates)
    writer.writerows(electrodes)
print('csv done')

# When visualizing with mayavi which uses numpy arrays, need to switch x and z coordinates.
