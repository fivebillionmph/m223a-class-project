# Phase Amplitude Coupling (pac)

import os
import matlab.engine

def run ():
    eng = matlab.engine.start_matlab()
    pac = eng.pac (r'C:\Users\alido\Desktop\2\EEG1.dat', matlab.double([2, 14]), matlab.double([40, 150]), nargout=2)
    print(pac)
