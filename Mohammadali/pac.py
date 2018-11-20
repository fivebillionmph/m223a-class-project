import matlab.engine
eng = matlab.engine.start_matlab()
pac = eng.pac (r'file', matlab.double([2, 14]), matlab.double([40, 150]), nargout=2)
print(pac)

