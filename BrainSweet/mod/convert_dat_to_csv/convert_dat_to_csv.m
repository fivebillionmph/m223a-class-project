function [] = convert_dat_to_csv(filename)

[signal,states,parameters]=load_bcidat([filename '.dat']);
temp=[single(states.StimulusCode),single(states.StimulusType),signal];
header=[parameters.SamplingRate.NumericValue];
header=padarray(header,[size(header,1),size(temp,2)]-size(header),'post');
temp=[header;temp];
csvwrite(filename+".csv",temp);