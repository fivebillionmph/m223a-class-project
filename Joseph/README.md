# Electrode Localization

## CT->MR Registration

**Function:**
Perform rigid-body registration using MRI as the fixed image and CT as the moving image using a series of optimizations and transformations from the SimpleITK toolbox for Python.

**Inputs:**
  *Preoperative MRI image and Post-operative CT image (both in NIfTI format)

**Outputs:**
  * Registered CT image (NIfTI format)

**Language:**
  * Python 3.6

Dependencies:
  * pip install SimpleITK


## Electrode Detection

**Function:**
Finds electrode locations from the registered CT image (produced from the above step) by thresholding, Gaussian blurring, and finding the centroids of connected components filtered by pixel-size.

**Inputs:**
  * Registered CT (NIfTI format)

**Outputs:**
  * Electrode locations in .csv format

**Language:**
  * Python 3.6

**Dependencies:**
  * pip install SimpleITK
  * import csv


## Talairach->MR Registration

**Function:**
Converts Talairach coordinates to MNI coordinates using [mni2tal](https://bioimagesuiteweb.github.io/webapp/mni2tal.html) from Yale BioImage Suite in order to to plot in MR space using the open source MNI/ICBM 152 template which can be found [here](http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009).
This script uses Selenium to automate web browser interaction by the user.

**Inputs:**
  * Talairach coordinates in .csv format

**Outputs:**
  * MNI coordinates in .csv format (downloaded from mni2tal)

**Language:**
  * Python 3.6

**Dependencies:**
  * pip install SimpleITK
  * pip install Selenium
  * install ChromeDriver.exe [here](http://chromedriver.chromium.org/downloads)

**Notes**
  - Need to set environment PATH variable to where ChromeDriver.exe is
  - Currently only has been tested in a Windows environment
