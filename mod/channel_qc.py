"""
SIGNAL ANALYSIS: Channel QC (Amy Cummings "method 2")

This allows identification of faulty channels.
Written with python 3.6. sys.argv[1] is path to file, sys.argv[2] is file name.
Requires path to csv.
Applies notch filter to get power ratio (amount of time band in frequency is in range [0.5,30].
Good channel arbitrarily set at >0.8. 
Output table will include identification, channels, and binary outcome (1 for good channel, 0 for bad channel).

"""

import numpy as np
import pandas as pd
import scipy
from scipy import signal

METHOD = 2

def run(cursor, subject_id, filename):
    
    eeg = pd.read_csv(filename)
    Only_Channels = eeg.iloc[1:,2:]
    
    #removes electric interferance
    fs = 256.0
    f0 = 60.0
    Q = 30.0
    w0 = f0/(fs/2)
    b, a = scipy.signal.iirnotch(w0, Q)
    Y = signal.filtfilt(b, a, Only_Channels)
    
    #determines amount of time EEG with appropriate returns
    def bin_power(X, Band, Fs):
        C = np.fft.fft(X)
        C = abs(C)
        Power = np.zeros(len(Band) - 1)
        for Freq_Index in range(0, len(Band) - 1):
            Freq = float(Band[Freq_Index])
            Next_Freq = float(Band[Freq_Index + 1])
            Power[Freq_Index] = sum(
                C[int(np.floor(
                    Freq / Fs * len(X)
                )): int(np.floor(Next_Freq / Fs * len(X)))]
            )
        Power_Ratio = Power / sum(Power)
        return Power, Power_Ratio
    
    #prints channel values
    for x in range(0,32,1):
        print([x],[((bin_power(Y[:,x], [0.5,30], 256))[1][0])])
        insert_scores = "INSERT INTO scores(sid,channel,method,score0) VALUES(%s, %s, %s, %s);"
        cursor.execute(insert_scores, (subject_id, x + 1, METHOD, (bin_power(Y[:,x], [0.5,30], 256))[1][0]))
