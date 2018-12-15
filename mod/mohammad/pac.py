import matlab.engine

def run(eeg_file, band_lo, band_hi, ch_count,
                             ch_first, ch_last, sigtime_total, sigtime_window, sigtime_step):
    eng = matlab.engine.start_matlab()
    print("Checkpoint 3")
    pac = eng.pac(eeg_file, matlab.double(band_lo), matlab.double(band_hi), float(ch_count), float(ch_first),
                   float(ch_last), float(sigtime_total), float(sigtime_window), float(sigtime_step), nargout=2)
    print("Checkpoint 4")