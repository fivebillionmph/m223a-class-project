'''
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
from math import *
import winpython as winp
import sympy as sympy
import matplotlib.pyplot as plt
import numpy as numpy
import random as random
import scipy as sp
import xlrd as xlrd
import pandas as pd
from scipy.fftpack import fft,ifft
import importlib
import sys 
import os
sys.path.append(os.path.abspath("C:\\Users\dell\\Desktop\\FALL2018\\223A\\Project"))
from read_wave_to_list import *
from read_raw_signal_file import *
from return_raw_file_name import * #return_raw_file_name(channel_number)
from signal_cancel_dc import *
from signal_filter import *
'''
def signal_compression(original_signal, point_range,startpoint,endpoint):#return: int_list
    counter = 0
    signal_after_compression = []
    score = 0
#    print("calculation round = ", round_cal)
    for i in range(int((endpoint-startpoint)/point_range)): #calculation round
#        print("Now doing round = ", )
        score = 0
        for j in range(2*point_range):
            score  = score + original_signal[startpoint+j+i*point_range]/(2*point_range)
        signal_after_compression .append(score)
    print("Compression finished")
    return(signal_after_compression)

#testbench

'''
startpoint = 0
endpoint = 300000
point_range = [50,100,150,200]
channel_name = 4
sampling_rate = 9600
transition_width = 50 #Hz
cutoff_hz = 100
signal_file_name = return_raw_file_name(channel_name)
raw_signal =  read_raw_signal_file(signal_file_name)
signal_canceldc_result = signal_cancel_dc(raw_signal[startpoint:endpoint])
signal_filtered = signal_filter(signal_canceldc_result,sampling_rate, transition_width, cutoff_hz)

#signal_after_compress_1 = signal_compression(signal_filtered, point_range[0])
#signal_after_compress_2 = signal_compression(signal_filtered, point_range[1])
signal_after_compress_3 = signal_compression(signal_filtered, point_range[2])
signal_after_compress_4 = signal_compression(signal_filtered, point_range[3])
#print(len(signal_after_compress_1))
pl.subplot(321)
pl.plot(np.arange(startpoint,endpoint,1), signal_canceldc_result)
pl.subplot(322)
pl.plot(np.arange(startpoint,endpoint,1), signal_filtered)
pl.title('Signal After Filtering')

#pl.subplot(233)
#pl.plot(np.arange(startpoint,endpoint-point_range[0], point_range[0]), signal_after_compress_1)
#pl.plot(np.arange(startpoint,endpoint,1), signal_canceldc_result)
#pl.title('Signal Compression rate:1/%d'% point_range[0])
#pl.subplot(234)
#pl.plot(np.arange(startpoint,endpoint-point_range[1], point_range[1]), signal_after_compress_2)
#pl.plot(np.arange(startpoint,endpoint,1), signal_canceldc_result)
#pl.title('Signal Compression rate:1/%d'% point_range[1])
pl.subplot(311)
pl.plot(np.arange(startpoint,endpoint-point_range[2], point_range[2]), signal_after_compress_3)
#pl.plot(np.arange(startpoint,endpoint,1), signal_canceldc_result)
pl.title('Signal Compression rate:1/%d'% point_range[2])
pl.subplot(312)
pl.plot(np.arange(startpoint,endpoint-point_range[3], point_range[3]), signal_after_compress_4)
#pl.plot(np.arange(startpoint,endpoint,1), signal_canceldc_result)
pl.title('Signal Compression rate:1/%d'% point_range[3])
pl.show()


'''
    
