%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Phase Amplitude Coupling (PAC) %%%%%
function [MaxPAC, MeanPAC] = pac(file, LowFreqs, HighFreqs)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

isUseParallel = 0;
isUseMex = 0;
numfreqs = 0;

%%%%% Input Data %%%%%

[filepath, name, ext] = fileparts(file);

if strcmpi(ext, '.dat')
    % % % EEG&ECOG
    [signal, ~, parameters, ~] = load_bcidat (file);
    F = transpose (signal);
    sRate = parameters.SamplingRate.NumericValue;
    % % % Using just 1 min. of ECOG! (otherwise, Out of memory (OOM))
%     F = F(:,1:576000); % % % time: [(1/9600)*X(iteration)=60s]
elseif strcmpi(ext, '.edf')
     % % % .edf file format
     [hdr, record]= edfread(file);
     F = record;
     sRate = hdr.frequency(1,1);
     % % % Using just 2 min. of EDF!
     F = F(:,1:240000); % % % time: [(1/2000)*X(iteration)=120s]
else
    Error ('Invalid File Format');
end

% % % Frequency Ranges for Low and High Oscillations

% LowFreqs = [2 14];
% HighFreqs = [40 150];

%%%%% Calculating PAC %%%%%

% % % m: number of the first signal to calculate MaxPAC
m = 1;
% % % n:number of the second signal to calculate MaxPAC
n = 1;
% % % z:number of used signals to calculate MaxPAC (one by one)
% z = n-m+1;

MaxPAC = (n);
MeanPAC = (n);

for i = m:n

[sPAC, ~, ~] = bst_pac (F(i,:), sRate, LowFreqs, HighFreqs, isUseParallel, isUseMex, numfreqs);

MaxPAC (i) = max (max (max (sPAC(:,1,:,:))));
MeanPAC (i) = mean (mean (mean (sPAC(:,1,:,:))));

%%%%% Ploting the PAC (not necessary for the project) %%%%%

% subplot (2,z,i+z-n)
% plot (F(i,:));
% title (['Signal:', num2str(i)]);
% xlabel ('Time');
% ylabel ('Frequency (Hz)');
% subplot (2,z,i+2*z-n)
% pcolor (squeeze(sPAC));
% colormap (jet);
% colorbar;
% title ({['MaxPAC=', num2str(MaxPAC)];['MeanPAC=', num2str(MeanPAC)]});
% xlabel ('Frequency for Amplitude (Hz)');
% ylabel ('Frequency for Phase (Hz)');

end

%%%%% Output Data %%%%%

MaxPAC = transpose (MaxPAC);
MeanPAC = transpose (MeanPAC);
Output = [MaxPAC, MeanPAC];

% csvwrite('Max_PAC.dat',MaxPAC);
% csvwrite('Mean_PAC.dat',MeanPAC);

csvfile = strcat(filepath,'\',name,'.csv');
csvwrite(csvfile, Output);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


