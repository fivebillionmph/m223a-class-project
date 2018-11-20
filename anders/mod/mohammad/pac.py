# Phase Amplitude Coupling (pac)

import os
import matlab.engine

def run ():
    eng = matlab.engine.start_matlab()
    pac = eng.pac (r'file', matlab.double([2, 14]), matlab.double([40, 150]), nargout=1)
    print(pac)
