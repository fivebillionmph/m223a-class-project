function [] = Power_Analysis(sid,file,startTime,stopTime,intervals,startFrequency,stopFrequency)

%%%input file, time interval, and frequency interval
%%%file includes location, name, and extension
%%%Outputs vector of Relative Power for all channels over specified time
%%%and frequency intervals

if (isnumeric(startTime))
else
    startTime =str2double(startTime);
end

if (isnumeric(stopTime))
else
    stopTime = str2double(stopTime);
end

if (isnumeric(intervals))
else
    intervals = str2double(intervals);
end

if (isnumeric(startFrequency))
else
    startFrequency = str2double(startFrequency);
end

if (isnumeric(stopFrequency))
else
    stopFrequency = str2double(stopFrequency);
end



%%%Determines the file type of the input file
[filepath,name,ext] = fileparts(file);
if (strcmp (ext,'.dat'))
    [Data,~,parameters] = load_bcidat(file);
    samplingFrequency = parameters.SamplingRate.NumericValue;
elseif (strcmp (ext,'.edf'))
   %filename = strcat(name,ext);
   [parameters,Data] = edfreadUntilDone(file);
   %[j,k] = size(parameters.frequency);
   %b = 1;
   %while ( b <= j)
   %     [~,Data(b,:)] = edfreadUntilDone(file,'targetSignals',b);
   %     b = b+1;
   %end
   samplingFrequency = parameters.frequency(1,1);
   Data = Data'; %transpose the data so it matches the bci type
else 
    error ('Unsupported file type')
end


%samplingFrequency = 256; %Used for testing

Fs = samplingFrequency;    %sampling frequency extracted from data type
Fc = Fs/2;  %folding frequency is the max frequency that can be found

%startFrequency = 0;  %Used for testing
%stopFrequency = 128;  %Used for testing


[m,n] = size(Data); %gives the size of the full data matrix

%%%Used to put all data types into type single to avoid issues with fft and
%%%memory size
tf = isa(Data,'single');
k = 1;
if (tf ~= true)
    while(k <= n)
    NewData(1:m,k) = cast(Data(1:m,k), 'single');
    k = k+1;
    end
    Data = NewData;
end

%%%Puts all of the input time points in terms of sample number
sampleTime = m/Fs;
%startTime = 0;  %Used for testing
trueStart = startTime*Fs;
if (trueStart == 0)
    trueStart = 1;
end
%stopTime = 202;  %Used for testing
trueStop = stopTime*Fs;
if (trueStop > sampleTime*Fs)
    trueStop = sampleTime*Fs;
end

Difference = trueStop-trueStart;
check = 0;
while (check < intervals)
    if (trueStop + Difference*check > sampleTime*Fs)
        intervals = check;
    end
    check = check + 1;
end

iterations = 0;
FinalData = ones(intervals,n);

while (iterations < intervals)
trueStart = trueStart + Difference*iterations;
trueStop = trueStop + Difference*iterations;
%%%Trims data to within confined timepoints
ConfinedData = (Data(trueStart:trueStop,1:n));
[m,n] = size(ConfinedData);

%sampleData = (Data(:,1)); %Used to test on smaller dataset
TransformData = fft(ConfinedData);

ConfinedData = [];  %sets matrix to empty matrix to free up memory

%%%Generates a frequency vector of equal stepsize up to folding frequency
Frequency = zeros(m/2,1);
i=1;
while (i<(m/2) || i==(m/2))
    Frequency(i,1) = Fs/m*i;
    i=i+1;
end


%%%Finds the start and stop frequencies in the matrix
startPoint = startFrequency*m/Fs;
round(startPoint);
if (startPoint == 0)
    startPoint = 1;
end
stopPoint = stopFrequency*m/Fs;
round(stopPoint);


%%%Manipulates the transform data to find the Power of each frequency
NormalizedData = TransformData.*1/(m);
TransformData = [];  %sets matrix to empty matrix to free up memory
NormalizedData = abs(NormalizedData).*(2^0.5);
MagnitudeData = NormalizedData(1:m/2,1:n);  %Magnitude of Fourier Amplitude
NormalizedData = [];  %sets matrix to empty matrix to free up memory
PowerData = MagnitudeData.^2;   %Power of Fourier Amplitude

%%%Data plotting
%plot(Frequency,MagnitudeData);
%PlotPowerData = PowerData(1:m/2,1:n);
%plot(Frequency,PlotPowerData);

MagnitudeData = [];  %sets matrix to empty matrix to free up memory


%%%Integrates the data using the trapezoidal method over the desired
%%%frequency band
PowerBand = trapz(Frequency(startPoint:stopPoint,1),PowerData(startPoint:stopPoint,1:n));

%%%Normalizes the data between zero and 1. Output of the program
OutputData = (PowerBand - min(PowerBand));
OutputData = (OutputData)./max(OutputData);
iterations = iterations + 1;
FinalData(iterations,:) = OutputData;
end

FinalData = FinalData';
%%%Writes the data to a csv of the same name and file location as input
csvfile = strcat(filepath,'\',name,ext,'-3.csv');
csvwrite(csvfile,FinalData); %generates a csv file as an output
