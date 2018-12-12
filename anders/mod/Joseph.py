# -*- coding: utf-8 -*-
"""
Trying SimpleITK
Created on Sun Nov 11 16:53:26 2018

@author: josep
"""

# from tkinter import Tk
# from tkinter.filedialog import askopenfilename
# from skimage import measure
import SimpleITK as sitk
from matplotlib import pyplot as plt

""" Read images """
def run(cursor, subject_id, CT_filename, MR_filename):
    moving_image = sitk.ReadImage(CT_filename)
    fixed_image = sitk.ReadImage(MR_filename)

    #interact(display_images, fixed_image_z=(0,fixed_image.GetSize()[2]-1), moving_image_z=(0,moving_image.GetSize()[2]-1), fixed_npa = fixed(sitk.GetArrayViewFromImage(fixed_image)), moving_npa=fixed(sitk.GetArrayViewFromImage(moving_image)));

    # fix up some image characteristics
    fixed_image.SetOrigin((0, 0, 0))
    fixed_image.SetDirection([1, 0, 0, 0, 1, 0, 0, 0, 1])
    fixed_image.SetSpacing([1, 1, 1])

    """ Initial alignment """
    initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                          moving_image, 
                                                          sitk.Euler3DTransform(), 
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)
    
    moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())
    
    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));
    
    """ registration """
    registration_method = sitk.ImageRegistrationMethod()
    
    # Similarity metric settings.
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
    registration_method.SetMetricSamplingPercentage(0.01)
    
    registration_method.SetInterpolator(sitk.sitkLinear)
    
    # Optimizer settings.
    registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    registration_method.SetOptimizerScalesFromPhysicalShift()
    
    # Setup for the multi-resolution framework.            
    registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
    registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
    registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()
    
    # Don't optimize in-place, we would possibly like to run this cell multiple times.
    registration_method.SetInitialTransform(initial_transform, inPlace=False)
    
    # Connect all of the observers so that we can perform plotting during registration.
    # registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
    # registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
    # registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations)
    # #registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))
    
    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32), 
                                                  sitk.Cast(moving_image, sitk.sitkFloat32))
    
    """ Post-registration analysis """
    print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
    print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
    moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())
    #interact(display_images_with_alpha, image_z=(0,fixed_image.GetSize()[2]), alpha=(0.0,1.0,0.05), fixed = fixed(fixed_image), moving=fixed(moving_resampled));
    
    rct_file = os.path.join(os.path.dirname(os.path.realpath(CT_filename)), 'registered'+'.nii.gz')
    sitk.WriteImage(moving_resampled, rct_file)
    cursor.execute("UPDATE subjects SET rct_path = %s WHERE sid = %s", (rct_file, subject_id))


################## ELECTRODE DETECTION #####################

    # Tk().withdraw()
    # filename = askopenfilename(title = "Select registered image")
    image = sitk.ReadImage(rct_file)

    # fix up some image characteristics
    image.SetOrigin((0, 0, 0))
    image.SetDirection([1, 0, 0, 0, 1, 0, 0, 0, 1])
    image.SetSpacing([1, 1, 1])

    # Cast/normalize to an image with a 0-255 range
    image_255 = sitk.Cast(sitk.RescaleIntensity(image), sitk.sitkUInt8)

    # Get information on image intensity distribution
    intensities = []

    for i in range(image.GetWidth()):
        for j in range(image.GetHeight()):
            for k in range(image.GetDepth()):
                intensities.append(image_255.GetPixel(i, j, k))

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
    attempt = np.column_stack([x, y, z])

    # rotate by 90 degrees towards the xy plane and 45 degrees towards yz plane
    theta = np.radians(90)
    c, s = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    rotated = np.dot(attempt, rotation_matrix)

    # rotate yz plane clockwise 45 degrees
    yz_tempt = rotated[:,[1,2]]
    theta = np.radians(45)
    c,s = np.cos(theta), np.sin(theta)
    rotation_matrix = np.array([[c,-s], [s,c]])
    yz_rotated = np.dot(yz_tempt, rotation_matrix)
    rotated[:,[1,2]] = yz_rotated
    
    rotated[:, 0] += image.GetWidth()-30
    rotated[:, 1] -= 75
    rotated[:, 2] += 130

    # save electrode locations in csv format
    # import csv
    # with open('electrode_coordinates.csv', mode='w', newline='') as electrode_coordinates:
    #     writer = csv.writer(electrode_coordinates)
    #     writer.writerows(rotated)
    # print('csv done')
        ## update to push to database channels table
        ## then, Yannan's electrode_position_correction will update these values again


    #####################################################################
    ###################Update Database###################################
    #####################################################################

    insert_channels = "INSERT channels SET x=%s, y=%s, z=%s WHERE sid = %s;"

    for i in range(len(rotated)):
        cursor.execute(insert_channels, (int(rotated.iloc[:, 0][i]),
                                         int(rotated.iloc[:, 1][i]),
                                         int(rotated.iloc[:, 2][i]), subject_id))
