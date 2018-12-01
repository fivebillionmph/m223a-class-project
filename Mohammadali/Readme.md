Signal Classification
Phase Amplitude Coupling (PAC)


Programming Language: MATLAB
(There is also a Python Command to run the MATLAB function.)

This Code seeks to show how the phase amplitude coupling (PAC) can be calculated as a part of the classification of brain signals. In fact, Modulation Index (MI) is the method being used here to calculate PAC.

This function accepts EEG and ECOG data files as well as European Data Format (EDF) ones. 
EEG data files can be handled well. However, ECOG and EDF files are too large and depending on the computer configuration, a part of the signal can be analyzed to find the MaxPAC and MeanPAC values.

Functions:

Main Function:
-	pac.m

Required Functions:
-	load_bcidat.m
-	load_bcidat.mexw64
-	edfread.m
-	bst_pac.m
-	bst_get.m
-	bst_chirplet.m
-	bst_bsxfun.m
-	bst_bandpass_fft.m

Inputs:
- file: Includes the path name, file name, and extension for the specified file.
- low_freqs: Candidate frequency band of slow oscillation e.g. [1 40] Hz.
- high_freqs: Candidate frequency band of fast oscillation e.g. [40 200] Hz.
- num_sig: Checks whether you have not chosen the wrong signal number (not more than all the available signals).
  Note: It should be bigger that the "last_sig"!
  Note: Use 0 if you want to calculate all the available signals; in this case, the values of "first_sig" and "last_sig" are not important.
- first_sig: Number of the first signal to calculate PAC.
- last_sig: Number of the last signal to calculate PAC.
- t_total: The total time period that you want to calculate PAC for each signal.
  Note:
- t_window: The short time period window that you want to calculate PAC for each signal.
- t_step: The time step between The short time period windows

Outputs:
- MaxPAC: Maximum value of PAC measures
- MeanPAC: Average value of PAC measures

The MATLAB command:
- [MaxPAC, MeanPAC] = pac(file, low_freqs, high_freqs, num_sig, first_sig, last_sig, t_total, t_window, t_step)
e.g. [MaxPAC, MeanPAC] = pac ('file', [2,14], [40,150], 5, 2, 4, 2, 1, 0.5)

The Python command:
- import matlab.engine
- eng = matlab.engine.start_matlab()
- pac = eng.pac (r'file', matlab.double([2, 14]), matlab.double([40, 150]), float(5), float(2), float(4), float(2), float(1), float(0.5), nargout=2)
- print(pac)
