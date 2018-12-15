import matlab.engine
eng = matlab.engine.start_matlab()
convert_dat_to_csv = eng.convert_dat_to_csv ('EEG1', nargout=0)

