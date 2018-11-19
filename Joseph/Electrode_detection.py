# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 11:01:04 2018

@author: josep
"""
# Call a GUI for user to select image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import SimpleITK as sitk
from skimage import measure
from matplotlib import pyplot as plt

Tk().withdraw()
filename = askopenfilename(title = "Select registered image")
image = sitk.ReadImage(filename)

# Cast/normalize to an image with a 0-255 range
image_255 = sitk.Cast(sitk.RescaleIntensity(image), sitk.sitkUInt8)

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

# Hard-coded threshold based on intensity histogram results
thresholded_image = image_255 > 200
sitk.WriteImage(thresholded_image, 'thresholded_image'+'.nii.gz')


"""
# Find connected components using skimage
nda = sitk.GetArrayFromImage(thresholded_image)
cc = measure.label(nda)
print(cc)
"""

"""
# Find connected components using SimpleITK
cc = sitk.ConnectedComponent(thresholded_image)

stats1 = sitk.LabelShapeStatisticsImageFilter()
stats1.Execute(sitk.ConnectedComponent(thresholded_image))

label_sizes_1 = [stats1.GetNumberOfPixels(l) for l in stats1.GetLabels() if l != 1]

plt.hist(label_sizes_1)
plt.title("Distribution of Object Sizes without cleanup")
plt.xlabel("Size in pixels")
plt.ylabel("Number of objects")
plt.show()
"""

# Set pixels that are in [min_intensity,otsu_threshold] to inside_value, values above otsu_threshold are
# set to outside_value. The sphere's have higher intensity values than the background, so they are outside.
otsu_filter = sitk.OtsuThresholdImageFilter()
otsu_filter.SetInsideValue(0)
otsu_filter.SetOutsideValue(255)
seg = otsu_filter.Execute(thresholded_image)

inside_value = 0
outside_value = 255
number_of_histogram_bins = 100
mask_output = True
mask_value = 255

sitk.WriteImage(seg, 'otsu'+'.nii.gz')

print(otsu_filter.GetThreshold())

# Find connected components
cc = sitk.ConnectedComponent(seg)

# Initiate empty lists to hold centroids or electrode locations and radii of electrode pixels
centroids = []
radii = []

# Estimate the sphere radius from the segmented image using the LabelShapeStatisticsImageFilter.
for i in range(256):
    mask = sitk.Image(cc[i].GetSize(), sitk.sitkUInt8)
    mask.CopyInformation(cc[i])
    
    for i in range(cc[i].GetWidth()):
        for j in range(cc[i].GetHeight()):
            for k in range(cc[i].GetDepth()):
                if cc[i].GetPixel(i,j,k) > 200:
                    mask.SetPixel(i,j,k, mask_value)
    
    labeled_result = sitk.OtsuThreshold(cc[i], mask, inside_value, outside_value, 
                                   number_of_histogram_bins, mask_output, mask_value)
    
    label_shape_analysis = sitk.LabelShapeStatisticsImageFilter()
    label_shape_analysis.SetBackgroundValue(0)
    label_shape_analysis.Execute(labeled_result)
    centroids.append((label_shape_analysis.GetCentroid(255)))
    radii.append((label_shape_analysis.GetEquivalentSphericalRadius(255)))

"""
# Clean up by filling holes and removing small connected components
vectorRadius = (1, 1, 1)
kernel = sitk.sitkBall
thresholded_image_with_opening = sitk.BinaryMorphologicalOpening(thresholded_image, vectorRadius, kernel)
sitk.WriteImage(thresholded_image_with_opening, 'thresholded_image_with_opening' + ".nii.gz")

stats2 = sitk.LabelShapeStatisticsImageFilter()
stats2.Execute(sitk.ConnectedComponent(thresholded_image_with_opening))

label_sizes_2 = [stats2.GetNumberOfPixels(l) for l in stats2.GetLabels() if l != 1]

plt.hist(label_sizes_2)
plt.title("Distribution of Object Sizes with opening")
plt.xlabel("Size in pixels")
plt.ylabel("Number of objects")
plt.show()

thresholded_image_with_opening_and_closing = sitk.BinaryMorphologicalClosing(thresholded_image_with_opening, vectorRadius, kernel)
sitk.WriteImage(thresholded_image_with_opening_and_closing, 'thresholded_image_with_opening_and_closing'+'.nii.gz')

stats3 = sitk.LabelShapeStatisticsImageFilter()
stats3.Execute(sitk.ConnectedComponent(thresholded_image_with_opening_and_closing)

label_sizes_3 = [stats3.GetNumberOfPixels(l) for l in stats3.GetLabels() if l != 1]

plt.hist(label_sizes_3)
plt.title("Distribution of Object Sizes minus artifact and closed")
plt.xlabel("Size in pixels")
plt.ylabel("Number of objects")
plt.show() """

# Find centroid for connected components

# try out sitk.Compose(img1, img2)

