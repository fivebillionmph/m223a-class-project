Signal Classification - Phase Amplitude Coupling (PAC)


•	Programming Language: MATLAB

•	This Code seeks to show how the phase amplitude coupling (PAC) can be calculated as a part of the classification of brain signals. In fact, Modulation Index (MI) is the method being used here to calculate PAC.

•	This function accepts EEG and ECOG data files as well as European Data Format (EDF) ones. 
EEG data files can be handled well. However, ECOG and EDF files are too large and depending on the computer configuration, a part of the signal can be analyzed. For example, the first one minute of the signal can be used to find the MaxPAC and MeanPAC.

•	Inputs:
- F: Signal time series [nSignals x nTime]
- sRate: Signal sampling rate (in Hz)
- bandNesting: Candidate frequency band of phase driving oscillations (low-frequency band) e.g., [1 40] Hz
- bandNested: Candidate frequency band of nested oscillations (high-frequency band) e.g., [40 200] Hz

•	Outputs:
- MaxPAC: Maximum value of PAC measures for all frequency pairs
- MeanPAC: Average value of PAC measures for all frequency pairs
