import matlab.engine
def run():
    eng = matlab.engine.start_matlab()
    pac = eng.pac (r'file', matlab.double([2, 14]), matlab.double([40, 150]), float(5), float(2), float(4), float(2), float(1), float(0.5), nargout=1)
    print(pac)

