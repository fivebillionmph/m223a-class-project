from find_index_by_time import *
def signal_cancel_dc(signal_raw,sampling_rate):
    signal_aver = 0
    signal_canceldc = []
    for i in range(len(signal_raw)):
        signal_aver = signal_aver + signal_raw[i]/len(signal_raw)
    for i in range(len(signal_raw)):
        signal_canceldc.append(signal_raw[i] - signal_aver)
    print("CANCELLING DC FINISHED")
    return(signal_canceldc)

def signal_cancel_dc_modified(inputtable,sampling_rate,starttime,endtime,calculation_level):
    calculation_level_inside_function = calculation_level+1
    space_string = ' '*calculation_level_inside_function
    signal_aver = 0
    signal_canceldc = []
    return_table = []
    #print(type(inputtable[0]))
    point = find_index_by_time(inputtable[0],starttime,endtime)
    return_table.append(inputtable[0][point['startpoint']:point['endpoint']])
    #print("returntable=",return_table)
    for i in range(point['startpoint'],point['endpoint']):
        signal_aver = signal_aver + inputtable[1][i]/(point['endpoint']-point['startpoint'])
    for i in range(point['startpoint'],point['endpoint']):
        signal_canceldc.append(inputtable[1][i] - signal_aver)
    return_table.append(signal_canceldc)
    print("{}{}".format(space_string,"Finished canceling DC"))
    #print(return_table)
    return(return_table)



'''
def find_index_by_time(time_table, starttime, endtime):
    if(starttime<time_table[0]):
        starttime_in_table = time_table[0]
    else:
        starttime_in_table = (starttime//(time_table[1]-time_table[0]))*(time_table[1]-time_table[0])
    if(endtime>time_table[len(time_table)-1]):
        endtime_in_table = time_table[len(time_table)-1]
    else:
        endtime_in_table = (endtime//(time_table[1]-time_table[0]))*(time_table[1]-time_table[0])
    startpoint = time_table.index(starttime_in_table)
    endpoint = time_table.index(endtime_in_table)
    return_dict = {'startpoint':startpoint,'endpoint':endpoint}
    return(return_dict)
'''
'''
point = find_index_by_time([7,10,14,16],6,18)
print(point)
'''
