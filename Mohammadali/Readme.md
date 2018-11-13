Signal Classification - Phase Amplitude Coupling (PAC)


•	Programming Language: MATLAB

•	This Code seeks to show how the phase amplitude coupling (PAC) can be calculated as a part of the classification of brain signals. 
In fact, Modulation Index (MI) is the method being used here to calculate PAC.

•	This function accepts EEG and ECOG data files as well as European Data Format (EDF) ones. 
EEG data files can be handled well. However, ECOG and EDF files are too large and depending on the computer configuration, a part of 
the signal can be analyzed. For example, the first one minute of the signal can be used to find the MaxPAC and MeanPAC values.

•	Functions:

Main Function:
pac.m

Required Functions:
load_bcidat.m
load_bcidat.mexw64
edfread.m
bst_pac.m
bst_get.m
bst_chirplet.m
bst_bsxfun.m
bst_bandpass_fft.m

•	Inputs:
- File name: Including the path name, file name, and extension for the specified file.

•	Outputs:
- MaxPAC: Maximum value of PAC measures
- MeanPAC: Average value of PAC measures

•	The MATLAB command would be:
[MaxPAC, MeanPAC] = pac ('C:\Users\alido\Desktop\2\EEG1.dat')

•	The Python command would also be:
import matlab.engine
eng = matlab.engine.start_matlab()
pac = eng.pac (r'C:\Users\alido\Desktop\2\EEG1.dat', nargout=2)
print(pac)
