Signal Classification - Phase Amplitude Coupling (PAC)

•	Programming Language: MATLAB

•	Functions:

Main one:
pac.m

Additional ones:
load_bcidat.m
load_bcidat.mexw64
edfread.m
bst_pac.m
bst_get.m
bst_chirplet.m
bst_bsxfun.m
bst_bandpass_fft.m

•	This Code seeks to show how the phase amplitude coupling (PAC) can be calculated as a part of the classification of brain signals. In fact, Modulation Index (MI) is the method being used here to calculate PAC.

•	This function accepts EEG and ECOG data files as well as European Data Format (EDF) ones. 
EEG data files can be handled well. However, ECOG and EDF files are too large and depending on the computer configuration, a part of the signal can be analyzed. For example, the first one minute of the signal can be used to find the MaxPAC and MeanPAC values.

•	Inputs:
- File name: Including the path name, file name, and extension for the specified file.
- Low-Frequency Band: Candidate frequency band of phase driving oscillations e.g., [1 40] Hz
- High-Frequency Band: Candidate frequency band of nested oscillations e.g., [40 200] Hz

•	Outputs:
- MaxPAC: Maximum value of PAC measures
- MeanPAC: Average value of PAC measures

•	The MATLAB command would be something as follows:
[MaxPAC, MeanPAC] = pac ('C:\Users\alido\Desktop\3\EEG1.dat', [2,14], [40,150])
