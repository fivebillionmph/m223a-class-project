## Band Power Over Time
#### Function Name:
- Power_Analysis_2.exe (same as above with added interval function)

#### Outline of Function:
- Trims input channel data to desired time interval
- Transforms Data for each channel from time domain to frequency domain using Fast Fourier Transform
- Integrates over the desired frequency range
- Normalizes data from 0 to 1
- Returns relative power for each channel over desired time and frequency interval
- 2nd function repeats the process for the number of specified time intervals

#### Calling function:
- MATLAB compiled executable

#### Inputs:
- File
  - Requires:
    - Path
    - Name
    - Extension
- Time Interval
  - Start Time
  - Stop Time
- Number of intervals (only for Power_Analysis_2.exe)
- Frequency Band
  - Lowest Frequency
  - Highest Frequency
  
#### Outputs:
- Relative Power of each channel over the desired time and frequency range
  - [1xn] Vector for Power_Analysis.exe
  - [mxn] Vector for Power_Analysis_2.exe
    - m = number of time intervals
    - n = number of channels
- Can generate a csv of the same name and location of input file

#### Language:
- Matlab

#### Additional files:
- To run in Matlab requires:
  - load_bcidat
    - Requires .mex file from Box
  - edfreadUntilDone
- Executable should not need additional files

#### Additional Notes
- Large data sets can cause function to crash due to lack of memory space
- edf data takes a long time to read
