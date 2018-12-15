import csv
import numpy as np
#def read_raw_signal_file(csv_filename,parameter_signal,calculation_level):
def read_raw_signal_file(csv_filename,sampling_rate,calculation_level):
    calculation_level_inside_function = calculation_level+1
    signal_raw = []
    return_table = []
    #sampling_rate = parameter_signal['sampling_rate']
    space_string = ' '*calculation_level_inside_function
    #print('{}{}{}'.format('hello',space_string,'hello'))
    with open(csv_filename) as channel1:
        reader = csv.reader(channel1)
        #print(reader)
        #next(reader) #skip header
        for row in reader:
            signal_raw.append(float(row[0]))
        channel1.close()
    print("{}{}{}".format(space_string,"Finished reading signal from ",csv_filename))
    time_table = np.arange(0,len(signal_raw)/sampling_rate,1/sampling_rate)
    time_table_final = np.array(time_table).tolist()
    #print(type(time_table))
    #print(type(time_table_final))
    return_table.append(time_table_final)
    return_table.append(signal_raw)
    return(return_table)

#Testbench
'''
parameter_signal = {'sampling_rate':9600}
a= read_raw_signal_file('ECOG_signal_data_channel1.csv',parameter_signal['sampling_rate'],3)
'''
'''
print(len(a[0]))
print(len(a[1]))
print(a[0][1])
print(a[1][1])

'''
