CT_MR_Registration

Outline of Function:
Rigid body registration using MR as the fixed image and CT as the moving image using a series of transformations and interpolation.

Inputs:
Preop MR Nifti file
Postop CT Nifti file

Outputs:
Registered Nifti file

Language:
Python 3.7.0

Dependencies:
pip install SimpleITK


Electrode Detection

Outline of Function:
Finds electrode locations from the registered CT-MR image produced above using simple thresholding and finding centroids of connected components.

Inputs:
Registered CT-MR Nifti file

Outputs:
Electrode locations

Language:
Python 3.7.0

Dependencies:
pip install SimpleITK

