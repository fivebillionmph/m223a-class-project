
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
from math import *
import winpython as winp
import sympy as sympy
import matplotlib.pyplot as plt
import numpy as numpy
import random as random
'''
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
'''

def signal_filter_lowpass(original_signal,sampling_rate, transition_width, cutoff_hz):
    t = arange(len(original_signal)) /sampling_rate
    # The Nyquist rate of the signal.
    nyq_rate = sampling_rate / 2.0
    # The desired width of the transition from pass to stop,
    # relative to the Nyquist rate.  We'll design the filter
    # with a 5 Hz transition width.
    width = transition_width/nyq_rate
    # The desired attenuation in the stop band, in dB.
    ripple_db = 60.0
    N, beta = kaiserord(ripple_db, width)
    # Use firwin with a Kaiser window to create a lowpass FIR filter.
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    print("Now doing filtering")
    print("-- Window: Kaiser")
    print("-- Sample points = ", len(original_signal), ", Sampling Rate = ", sampling_rate)
    print("-- Transition_width = ", transition_width)
    print("-- Cutoff_hz = ",cutoff_hz)
    # Use lfilter to filter x with the FIR filter.
    filtered_x = lfilter(taps, 1., original_signal)
    print("Filter Finished")
    return(filtered_x)

#TESTBENCH
'''

channel_name = 3
sampling_rate = 9600
transition_width = [50,100] #Hz
cutoff_hz = [100,200]
startpoint = 15000
endpoint = 17000
signal_file_name = return_raw_file_name(channel_name)
raw_signal =  read_raw_signal_file(signal_file_name)
signal_canceldc_result = signal_cancel_dc(raw_signal[startpoint:endpoint])
#time period
print(type(signal_canceldc_result[0]))
filtered_x = signal_filter(signal_canceldc_result,sampling_rate, transition_width[1], cutoff_hz[1])
t = arange(len(filtered_x)) /sampling_rate
pl.plot(t, filtered_x, 'g', linewidth=4)
pl.show()
'''    
    
'''
#------------------------------------------------
# Create a signal for demonstration.
#------------------------------------------------
channel_name = 3
sample_rate = 9600
transition_width = [50,100] #Hz
cutoff_hz = [100,200]
startpoint = 15000
endpoint = 17000
signal_file_name = return_raw_file_name(channel_name)
raw_signal =  read_raw_signal_file(signal_file_name)
signal_canceldc_result = signal_cancel_dc(raw_signal[startpoint:endpoint])
#time period
t = arange(len(signal_canceldc_result)) / sample_rate
print(type(signal_canceldc_result[0]))


#------------------------------------------------
# Create a FIR filter and apply it to x.
#------------------------------------------------

# The Nyquist rate of the signal.
nyq_rate = sample_rate / 2.0
print("nyq_rate =",nyq_rate)
# The desired width of the transition from pass to stop,
# relative to the Nyquist rate.  We'll design the filter
# with a 5 Hz transition width.
width = []
width.append(transition_width[0]/nyq_rate)
width.append(transition_width[1]/nyq_rate)
# The desired attenuation in the stop band, in dB.
ripple_db = 60.0

# Compute the order and Kaiser parameter for the FIR filter.
N0, beta0 = kaiserord(ripple_db, width[0])
N1, beta1 = kaiserord(ripple_db, width[1])
# The cutoff frequency of the filter.
#cutoff_hz = 10.0

# Use firwin with a Kaiser window to create a lowpass FIR filter.
taps0 = firwin(N0, cutoff_hz[0]/nyq_rate, window=('kaiser', beta0))
taps1 = firwin(N1, cutoff_hz[1]/nyq_rate, window=('kaiser', beta1))

# Use lfilter to filter x with the FIR filter.
filtered_x0 = lfilter(taps0, 1.0, signal_canceldc_result)
filtered_x1 = lfilter(taps1, 1.0, signal_canceldc_result)
#------------------------------------------------
# Plot the FIR filter coefficients.
#------------------------------------------------
'''
'''
pl.subplot(221)
w, h = freqz(taps0, worN=8000)
pl.plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlabel('Frequency (Hz)')
ylabel('Gain')
title('Frequency Response')
ylim(-0.05, 1.05)
grid(True)

pl.subplot(222)
delay0 = 0.5 * (N0-1) / sample_rate
# Plot the original signal.
#plot(t, signal_canceldc_result )
# Plot the filtered signal, shifted to compensate for the phase delay.
plot(t-delay0, filtered_x0, 'r-')
# Plot just the "good" part of the filtered signal.  The first N-1
# samples are "corrupted" by the initial conditions.
plot(t[N0-1:]-delay0, filtered_x0[N0-1:], 'g', linewidth=4)
xlabel('t')
title('filtered vs non-filtered')
grid(True)

pl.subplot(223)
w, h = freqz(taps1, worN=8000)
pl.plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlabel('Frequency (Hz)')
ylabel('Gain')
ylim(-0.05, 1.05)
grid(True)

pl.subplot(224)
delay1 = 0.5 * (N1-1) / sample_rate
# Plot the original signal.
#plot(t, signal_canceldc_result )
# Plot the filtered signal, shifted to compensate for the phase delay.
plot(t-delay1, filtered_x1, 'r-')
# Plot just the "good" part of the filtered signal.  The first N-1
# samples are "corrupted" by the initial conditions.
plot(t[N1-1:]-delay1, filtered_x1[N1-1:], 'g', linewidth=4)
xlabel('t')
grid(True)


pl.show()
'''

#------------------------------------------------
# Plot the magnitude response of the filter.
#------------------------------------------------
'''
figure(2)
clf()
w, h = freqz(taps, worN=8000)
plot((w/pi)*nyq_rate, absolute(h), linewidth=2)
xlabel('Frequency (Hz)')
ylabel('Gain')
title('Frequency Response')
ylim(-0.05, 1.05)
grid(True)
'''

#------------------------------------------------
# Plot the original and filtered signals.
#------------------------------------------------
'''
# The phase delay of the filtered signal.
delay = 0.5 * (N-1) / sample_rate

figure(3)
# Plot the original signal.
plot(t, signal_canceldc_result)
# Plot the filtered signal, shifted to compensate for the phase delay.
plot(t-delay, filtered_x, 'r-')
# Plot just the "good" part of the filtered signal.  The first N-1
# samples are "corrupted" by the initial conditions.
plot(t[N-1:]-delay, filtered_x[N-1:], 'g', linewidth=4)

xlabel('t')
grid(True)
'''

