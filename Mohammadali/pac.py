import matlab.engine
eng = matlab.engine.start_matlab()
pac = eng.pac (r'C:\Users\alido\Desktop\3\EEG1.dat', matlab.double([2, 14]), matlab.double([40, 150]), nargout=1)
print(pac)
