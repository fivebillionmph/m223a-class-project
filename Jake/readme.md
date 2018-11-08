## Band Power Over Time
#### Outline of Function:
- Trims input channel data to desired time interval
- Transforms Data for each channel from time domain to frequency domain using Fast Fourier Transform
- Integrates over the desired frequency range
- Normalizes data from 0 to 1
- Returns relative power for each channel over desired time and frequency interval

#### Calling function:
- Currently a Matlab script
- Plan to convert to executable

#### Inputs:
- File
  - Requires:
    - Path
    - Name
    - Extension
- Time Interval
  - Start Time
  - Stop Time
- Frequency Band
  - Lowest Frequency
  - Highest Frequency
  
#### Outputs:
- Relative Power of each channel over the desired time and frequency range
  - [1xn] Vector
    - n = number of channels
- Can generate a csv of the same name and location of input file

#### Language:
- Matlab

#### Additional files:
- To run in Matlab requires:
  - load_bcidat
  - edfreadUntilDone
- Executable should not need additional files

#### Additional Notes
- Large data sets can cause function to crash due to lack of memory space
- edf data rakes a long time to read
