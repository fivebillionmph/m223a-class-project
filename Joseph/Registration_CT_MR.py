# -*- coding: utf-8 -*-
"""
Trying SimpleITK
Created on Sun Nov 11 16:53:26 2018

@author: josep
"""
import SimpleITK as sitk

""" Read images """
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
CT_filename = askopenfilename(title = "Select CT image")
MR_filename = askopenfilename(title = "Select MR image")

moving_image = sitk.ReadImage(CT_filename)
fixed_image = sitk.ReadImage(MR_filename)

# fix up some image characteristics
fixed_image.SetOrigin((0,0,0))
fixed_image.SetDirection([1,0,0,0,1,0,0,0,1])
fixed_image.SetSpacing([1,1,1])

""" Initial alignment """
initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                      moving_image, 
                                                      sitk.Euler3DTransform(), 
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

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
final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32), 
                                              sitk.Cast(moving_image, sitk.sitkFloat32))

""" Post-registration analysis """
print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))
moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())

sitk.WriteImage(moving_resampled, 'registered'+'.nii.gz')
