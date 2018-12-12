%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%% Phase Amplitude Coupling (PAC) %%%%%
function [MaxPAC, MeanPAC] = pac(file, low_freqs, high_freqs, num_sig, first_sig, last_sig, t_total, t_window, t_step)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

isUseParallel = 0;
isUseMex = 0;
numfreqs = 0;

%%%%% Input Data %%%%%

[filepath, name, ext] = fileparts(file);
ns = num_sig;

if strcmpi(ext, '.dat')
    % % % EEG&ECOG
    [signal, ~, parameters, ~] = load_bcidat (file);
    F = transpose (signal);
    [a, b] = size(F);
    sRate = parameters.SamplingRate.NumericValue;
    % % % Number of used signals (n) 
    if (ns == 0)
        n = a;
    elseif (ns < a)
        n = ns;
    elseif (a == ns)
        n = a;
    else
        Error ('Invalid Signal Number');
    end
    % % % Using just t min. of ECOG! (otherwise, Out of memory (OOM))
    if (t_total == 0)
        c = b;
    else
        c = sRate*60*t_total;
    end
    if (c <= b)
        F = F(1:n, 1:c);
    else
        Error ('Invalid Time Request');
    end

elseif strcmpi(ext, '.edf')
     % % % .edf file format
     [hdr, record]= edfread(file);
     F = record;
     [a, b] = size(F);
     sRate = hdr.frequency(1,1);
     % % % Number of used signals (n)
    if (ns == 0)
        n = a;
    elseif (ns < a)
        n = ns;
    elseif (a == ns)
        n = a;
    else
        Error ('Invalid Signal Number');
    end
     % % % Using just t min. of EDF!
    if (t_total == 0)
        c = b;
    else
        c = sRate*60*t_total;
    end
    if (c <= b)
        F = F(1:n, 1:c);
    else
        Error ('Invalid Time Request');
    end

else
    Error ('Invalid File Format');
end

% % % Frequency Ranges for Low and High Oscillations

% LowFreqs = [2 14];
% HighFreqs = [40 150];

%%%%% Calculating PAC %%%%%

% % % s: number of the first signal to calculate PAC
% % % e: number of the last signal to calculate PAC
if (ns == 0)
    s = 1;
    e = n;
else
    s = first_sig;
    e = last_sig;
end

tp = sRate*60*t_window;
ts = sRate*60*t_step;

G = zeros(n, tp);

if (t_total == 0)
    nn = floor(b/(sRate*60*t_window));
else
    nn = floor(t_total/t_window);
end

MaxPAC = zeros(n, nn);
MeanPAC = zeros(n, nn);

for i = s:e
    k = 1;
    p = 1;
    for j=tp:ts:c
        G (i, :) = F(i, p:j);
        [sPAC, ~, ~] = bst_pac (G(i, :), sRate, low_freqs, high_freqs, isUseParallel, isUseMex, numfreqs);

        MaxPAC (i, k) = max (max (max (sPAC(:,1,:,:))));
        MeanPAC (i, k) = mean (mean (mean (sPAC(:,1,:,:))));

        p = (k * ts) + 1;
        k = k + 1;               
    end
end

MaxPAC = MaxPAC (s:e, :);
MeanPAC =  MeanPAC (s:e, :);

%%%%% Output Data %%%%%

zero = zeros ((e - s + 1), 1);
Output = [MaxPAC zero MeanPAC];

csvfile = strcat(filepath,'\',name, ext, '-4.csv');
csvwrite(csvfile, Output);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


