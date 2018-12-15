import matlab.engine
def run(sig_file):
    eng = matlab.engine.start_matlab()
    convert_dat_to_csv = eng.convert_dat_to_csv (sig_file, nargout=0)

