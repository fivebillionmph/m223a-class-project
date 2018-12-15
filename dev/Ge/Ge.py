#def run(cursor, sid, ECoG_filepath)#
#output table: channel number - score0#
#need math, scipy, csv, sys, os
import scipy
import scipy.io as aio
import csv
import math
import numpy as np
import sys 
import os
from scipy.fftpack import fft,ifft
from scipy.stats.stats import pearsonr


import matlab.engine
#import pylab
method = 5
#import wrap1
#import function_wil_be_called
#data = matlab.engine.start_matlab()
#tf = data.load_bcidat('ECOG001S001R01.dat')
#print(type(tf))
import psycopg2
import psycopg2.extras

'''select_subject = """SELECT * from subjects WHERE name=%s"""
cursor.execute(select_subject, (name,))
subject_names = cursor.fetchall()
print(subject_names)
'''
ECoG_filepath = 'C:\\Users\\fangg027\\Downloads\\ECOG001S001R01.dat'
sid  = 1

def run(cursor, sid, ECoG_filepath):
    method = 5
    print("Initialization")
    ## folders setting #
    code_path = os.path.split(os.path.realpath(__file__))[0]
    dat_file_path = os.path.split(ECoG_filepath)[0]
    #print(dat_file_path)
    dat_file_name = os.path.split(ECoG_filepath)[1][:-4]
    #print(dat_file_name)
    print("code directory = ",code_path)
    print("dat file path = ",os.path.split(ECoG_filepath))
    csv_folder_name = "\\data for speech_correlation\\"
    csv_folder_path = '{}{}'.format(code_path,csv_folder_name)
    createFolder(csv_folder_path)
    print("data stored in =",csv_folder_path)
    # set channels need to analyse #
    #start_channel_input = 2
    start_channel_input = int(str(input("Start Channel(1-100):")))
    #end_channel_input = 10
    end_channel_input = int(str(input("End Channel(1-100):")))
    matlab_filename = matlabcode_generator(ECoG_filepath,csv_folder_path,start_channel_input,end_channel_input)
    print("Matlab code generated, now running matlab code....")
    #run matlab to convert .dat to csv
    eng = matlab.engine.start_matlab()
    eng.matlab_filename()
    eng.quit()
    print("CSV file for each channel created")
    # table setting #
    starttime_input = float(str(input("The start time of signal you wish to analyze (0-180):")))
    endtime_input = float(str(input("The end time of signal you wish to analyze (0-180):")))
    compressed_range = int(str(input("Compressed n point to one, input n(10-2000):")))
    parameter_signal = {'sampling_rate':9600,'start_channel':start_channel_input, 'end_channel':end_channel_input,'now_analysis_channel_number':61, 'signal_name_table':'-need to fill-','startpoint':96000,'endpoint':192000,'starttime':starttime_input,'endtime':endtime_input}
    parameter_powerband = {'powerband_range':compressed_range,'freq_low_limit':15, 'freq_high_limit':30,'round_of_powerband':5,'output_file':'{}{}{}'.format("powerband_circularshift of channel",parameter_signal['now_analysis_channel_number'],".csv")}
    parameter_powerband_frequency_table = [[2,40,10]]
    parameter_circularshift = {'shift_round':10,'shift_time':0.05,'result_output_csv':'20181126_circularshift_test2101.csv','mode_general':'w'}
    main_function(parameter_signal,parameter_powerband,parameter_circularshift,csv_folder_path,dat_file_name)
    csv_to_db = picking_result(parameter_signal,csv_folder_path)
    for i in range(len(csv_to_db[0])+1):
        insert_scores = "INSERT INTO scores(sid,channel,method,score0) VALUES(%s, %s, %s, %s);"
        cursor.execute(insert_scores, (sid, csv_to_db[0][i], method, csv_to_db[1][i]))

def main_function(parameter_signal,parameter_powerband,parameter_circularshift,csv_folder_path,dat_file_name):
    filename_adder = '_signal_channel_'
    calculation_level = 0
    csv_raw_file_path = '{}{}{}{}{}{}'.format(csv_folder_path,'\\',dat_file_name,filename_adder ,98,".csv")
    raw_signal =  read_raw_signal_file(csv_raw_file_path,parameter_signal['sampling_rate'],0)
    wave_binary(raw_signal[1],500,-500,0,len(raw_signal[0]), 500, 500,csv_folder_path)
    #def wave_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint, point_range, score,csv_folder_path):
    print("now doing wav compression")
    run_signal_compression(parameter_powerband['powerband_range'],csv_folder_path)
    for i in range(parameter_signal[ 'start_channel'],parameter_signal['end_channel']+1):
        channel_number = i
        parameter_signal['now_analysis_channel_number'] = i
        #channel_number = 61
        #parameter_signal['now_analysis_channel_number'] = 61
        print("now analyzing channel",channel_number)
        csv_raw_file_path = '{}{}{}{}{}{}'.format(csv_folder_path,'\\',dat_file_name,filename_adder,channel_number,".csv")
        raw_signal =  read_raw_signal_file(return_raw_file_name(parameter_signal['now_analysis_channel_number']),parameter_signal['sampling_rate'],calculation_level)
        signal_canceldc_result =signal_cancel_dc_modified(raw_signal,parameter_signal['sampling_rate'],parameter_signal['starttime'],parameter_signal['endtime'],calculation_level)
        #signal_canceldc_result = signal_cancel_dc(raw_signal)
        #signal_after_time_adjustment = time_adjustment("20181126_circularshift_test2101.csv",signal_canceldc_result,parameter_signal['now_analysis_channel_number'],parameter_signal['sampling_rate'], parameter_signal['starttime'], parameter_signal['endtime'])
        #print("postadjustment length",len(signal_after_time_adjustment ))
        powerband_result_beforetimeadjustment = bandpower_multiplefrequency(parameter_powerband,parameter_powerband_frequency_table, parameter_signal,signal_canceldc_result,csv_folder_path)
        circular_shift_piece(parameter_circularshift,parameter_powerband,parameter_signal,parameter_powerband_frequency_table,csv_folder_path)
    print("Calculation Finished")
        

def matlabcode_generator(ECoG_filepath, csv_folder_path, start_channelnumber,end_channelnumber):
    dat_file_path = os.path.split(ECoG_filepath)[0]
    #print(dat_file_path)
    dat_file_name = os.path.split(ECoG_filepath)[1][:-4]
    #print(dat_file_name)
    filename_adder = '_signal_channel_'
    matlabcode_filename = '{}{}{}'.format(os.path.split(os.path.realpath(__file__))[0],"\\matlabcode",".m") #generate a matlabcodes @python's code's folder
    
    f = open(matlabcode_filename,"w+")
    f.write('{}{}{}'.format("original = strcat('",ECoG_filepath,"');\n"))
    f.write('[signal, states, parameters] = load_bcidat(original);\n')
    print("generating wav file")
    csv_file_name = '{}{}{}{}{}'.format(' ',dat_file_name,filename_adder ,98,".csv")
    csv_file_path = '{}{}{}{}{}{}'.format(csv_folder_path,'\\',dat_file_name,filename_adder ,98,".csv")
    print(csv_file_path)
    if os.path.isfile(csv_file_path):
        print("CSV file for channel",98, "aready existed")
    else:
        print("Will create CSV file for channel",98)
        f.write('{}{}{}'.format("filename1 =' ",csv_file_path, "';\n"))
        f.write('{}{}{}{}'.format('csvwrite(filename1,','signal(:,',98,"));\n"))

    for i in range(start_channelnumber,end_channelnumber+1,1):
        csv_file_name = '{}{}{}{}{}'.format(' ',dat_file_name,filename_adder ,i,".csv")
        csv_file_path = '{}{}{}{}{}{}'.format(csv_folder_path,'\\',dat_file_name,filename_adder ,i,".csv")
        #print(csv_file_path)
        if os.path.isfile(csv_file_path):
            print("CSV file for channel",i, "aready existed")
        else:
            print("Will create CSV file for channel",i)
            f.write('{}{}{}'.format("filename1 =' ",csv_file_path, "';\n"))
            f.write('{}{}{}{}'.format('csvwrite(filename1,','signal(:,',i,"));\n"))
    f.close()
    return(matlabcode_filename)

#def run(cursor, sid):


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("folder created:",directory)
        else:
            print("folder existed:",directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



def circular_shift_piece(parameter_circularshift,parameter_powerband,parameter_signal,parameter_powerband_frequency_table, csv_file_path):#for single channel
    shift_round = parameter_circularshift['shift_round']
    shift_time = parameter_circularshift['shift_time'] #second
    print("shift_round,shift_time = ",shift_round,shift_time)
    #shift_point = shift_time*parameter_signal['sampling_rate']/parameter_powerband['powerband_range']
    shift_point = int(shift_time*parameter_signal['sampling_rate']/parameter_powerband['powerband_range'])
    print("shift_point = ",shift_point)
    shift_halfround = int(shift_round/2)
    shift_start = 0 - shift_halfround 
    start_channel = parameter_signal['start_channel']
    end_channel = parameter_signal['end_channel']
    sampling_rate = parameter_signal['sampling_rate']
    channel_number = parameter_signal['now_analysis_channel_number']
    print("channel number = ",channel_number)
    bandpowerfolder = csv_file_path
    bandpower_filepath = '{}{}{}{}{}{}'.format(bandpowerfolder,"\\bandpower_channel_",parameter_powerband['powerband_range'],"_",channel_number,".csv")
    #bandpower_filepath_another ='{}{}{}{}{}'.format(bandpowerfolder,"bandpower_channel_",parameter_powerband['powerband_range'],"_",channel_number,".csv")
    circularshift_result_filepath =  '{}{}{}{}'.format(bandpowerfolder,"circularshift_bandpower_channel_",channel_number,".csv")
    signal_canceldc_result = []
    wave_voiced_binary = []
    time_list_wav  = []
    pearsonr_result_final =[]
    
    ##read wave file
    wavefile_filepath = '{}{}{}{}'.format(bandpowerfolder,"wave_binary_compressed_",parameter_powerband['powerband_range'],".csv")
    with open(wavefile_filepath,newline='') as channel1:
        reader = csv.reader(channel1)
    #print(reader)
    #next(reader) #skip header
        for row in reader:
            time_list_wav.append(float(row[0]))
            wave_voiced_binary.append(float(row[1])*20)
            #next(reader)
        channel1.close()
    ##read powerband file
    with open(bandpower_filepath,newline='') as channel1:
        reader = csv.reader(channel1)
        i=0
        matrix=[]
        for row in reader:
            if(i==0):
               topic = row
            else:
                if(i==1):
                    axis_name = row
                else:
                    if(i==2):
                        column_name = row
                    else:
                        matrix.append(list(map(float, row)))
                        #results = list(map(int, results))
            i = i+1                        
            #next(reader)       
        channel1.close()
    powerband_table = (np.transpose(matrix)).tolist()
    print("topic = ",topic)
    #print("axis = ", axis_name)
    print("heading = ",column_name)
    powerband_number = len(powerband_table)-1
#get startpoint and endpoint of wav, and powerband
    point_range_wav =  find_index_by_time(time_list_wav, parameter_signal['starttime'], parameter_signal['endtime'])
    startpoint_wav = int(point_range_wav["startpoint"])
    endpoint_wav = int(point_range_wav["endpoint"])
    point_range_pb =  find_index_by_time(powerband_table[0], parameter_signal['starttime'], parameter_signal['endtime'])
    startpoint_pb = int(point_range_pb["startpoint"])
    endpoint_pb = int(point_range_pb["endpoint"])
    for round_number in range(powerband_number):
        pearsonr_result_r = []
        pearsonr_result_p = []
        for i in range(shift_round):
            pearsonr_result = pearsonr(powerband_table[round_number+1][(startpoint_pb):(endpoint_pb)], wave_voiced_binary[startpoint_wav+shift_point*(i+shift_start):endpoint_wav-1+shift_point*(i+shift_start)])
            pearsonr_result_r.append(pearsonr_result[0])
            pearsonr_result_p.append(pearsonr_result[1])
        #print("result = ",pearsonr_result_r)
    #    print(pearsonr_result_r)
        sorted_r = sorted(pearsonr_result_r)
        #parameter_powerband_frequency_table = [[2,70,30]] 
        single_round_result = [round_number*((parameter_powerband_frequency_table[0][1]-parameter_powerband_frequency_table[0][0])//parameter_powerband_frequency_table[0][2])+parameter_powerband_frequency_table[0][0]]
        #print("largest r = ",sorted_r[len(sorted_r)-1])
        r_index = pearsonr_result_r.index(sorted_r[len(sorted_r)-1])
        #print(r_index)
        r_timing = (r_index+shift_start)*shift_time
        r_p = pearsonr_result_p[r_index]
        single_round_result.append(0-r_timing)
        single_round_result.append(sorted_r[len(sorted_r)-1])
        single_round_result.append(r_p)
        #print(single_round_result)
        pearsonr_result_final.append(single_round_result)
        heading = ['Frequency band number','Time Shift(sec)','Correation','p-value']
        with open(circularshift_result_filepath, parameter_circularshift['mode_general'], newline = '') as f:
            writer = csv.writer(f)
            writer.writerows([heading])
            writer.writerows(pearsonr_result_final)
            #writer.writerows([pearsonr_result_timeshift])
        print("csv updated")
        f.close()
    return(pearsonr_result)

def fft_single_round(original_signal_piece, FFT_point_number):
    fft_result_abs = []
    fft_signal_raw = fft(original_signal_piece, FFT_point_number)
#    print("FFT result", fft_signal_raw)
    for i in range(len(fft_signal_raw)):           
        fft_result_abs.append(numpy.real(sqrt((numpy.real(fft_signal_raw[i]))**2+((numpy.imag(fft_signal_raw[i]))**2)/len(fft_signal_raw))))

def powerband_piece(original_signal, powerband_range, freq_low, freq_high, sampling_rate):
    round_number = int(len(original_signal)/powerband_range)
    #print(round_number)
    powerband_piece_result = []
    fft_single_round_result = []
    if ((len(original_signal) - round_number*powerband_range) ==0):
        original_signal = [0]*int(powerband_range/2) + original_signal +[0]*(int(powerband_range/2))
    else:
        fill_zero = powerband_range-(len(original_signal) - round_number*powerband_range)
        round_number = round_number+1
        original_signal = [0]*int(powerband_range/2) + original_signal +[0]*(fill_zero+int(powerband_range/2))
    for i in range(round_number):
        fft_single_round_result.clear()
        score = 0
        fft_single_round_result = fft_single_round(original_signal[i*powerband_range:(i+1)*powerband_range], sampling_rate)
        for j in range (freq_low,freq_high):
            score = score + fft_single_round_result[j]
        powerband_piece_result.append(score/(freq_high-freq_low)/sampling_rate)
    return(powerband_piece_result)

def find_index_by_time(time_list, starttime, endtime):
#    print(starttime)
#    print(endtime)
    if(starttime<time_list[0]):
#        print("1")
        starttime_in_table = time_list[0]
        startpoint = time_list.index(starttime_in_table)
    else:
#        print("2")
        starttime_in_table = ((starttime-time_list[0])//(time_list[1]-time_list[0]))*(time_list[1]-time_list[0])+time_list[0]
        for i in range(len(time_list)-1):
            if ((time_list[i]<= starttime_in_table) and (time_list[i+1]> starttime_in_table)):
                startpoint = i
 #               print("startpoint=" , startpoint)
 #       print("time_step=",time_list[1]-time_list[0])
    if(endtime>time_list[len(time_list)-1]):
#        print("3")
        endtime_in_table = time_list[len(time_list)-1]
        endpoint = time_list.index(endtime_in_table)
    else:
 #       print("4")
        endtime_in_table = ((endtime-time_list[0])//(time_list[1]-time_list[0]))*(time_list[1]-time_list[0])+time_list[0]
        for i in range(len(time_list)-1):
            if ((time_list[i]< endtime_in_table) and (time_list[i+1]>= endtime_in_table)) :
                endpoint = i
#        print("endtime = ",endtime)
#        print("zhengshu = ", (endtime-time_list[0])//(time_list[1]-time_list[0]))
#        print("yushu = ",(endtime-time_list[0])%(time_list[1]-time_list[0]))
#        print('endtime_in_table,',endtime_in_table)
    #startpoint = time_list.index(starttime_in_table)
    #endpoint = time_list.index(endtime_in_table)
    return_dict = {'startpoint':startpoint,'endpoint':endpoint}
    return(return_dict)


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


def signal_compression(original_signal, point_range,startpoint,endpoint):#return: int_list
    counter = 0
    signal_table = []
    #signal_table.append(numpy.)
    signal_after_compression = []
    score = 0
#    print("calculation round = ", round_cal)
    for i in range(int((endpoint-startpoint)/point_range)): #calculation round
#        print("Now doing round = ", )
        score = 0
        for j in range(2*point_range):
            score  = score + original_signal[startpoint+j+i*point_range]/(2*point_range)
        signal_after_compression .append(score)
    print("Compression finished")
    return(signal_after_compression)

def run_signal_compression(point_range,csv_file_path):
    wave_voiced_binary = []
    with open('{}{}'.format(csv_file_path,"Binary wave.csv"),newline='') as channel1:
            reader = csv.reader(channel1)
        #print(reader)
        #next(reader) #skip header
            for row in reader:
                wave_voiced_binary.append(float(row[0]))
                #next(reader)
            channel1.close()
    startpoint = 0
    endpoint = len(wave_voiced_binary)
    print("endpoint = ", endpoint)
    signal_after_compression = signal_compression(wave_voiced_binary, point_range,startpoint,endpoint-point_range)
    time_list = []
    counter = 0
    for i in range(len(wave_voiced_binary)-point_range*2):
        if (counter == 0):
            time_list.append(i/9600)
        counter = counter +1
        if (counter ==point_range):
            counter = 0
    csv_table = [time_list, signal_after_compression]
    csv_table_t = np.transpose(csv_table)
    print(len(csv_table))
    print(len(csv_table_t))
    print(len(time_list))
    print(len(signal_after_compression))
    outputfolder = csv_file_path
    
    wavefile_filepath = '{}{}{}{}'.format(outputfolder,"wave_binary_compressed_",point_range,".csv")
    with open(wavefile_filepath,"w", newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(np.transpose(csv_table))
        #writer.writerows(csv_table)
    print("csv updated")
    f.close()
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

def wave_convert_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint):
    print('len_wavedata=', len(wave_data))
    wave_voiced_bi = []
#    for i in range(len(wave_data)):
    for i in range(endpoint-startpoint):
        if (wave_data[startpoint+i]> thh_positive or wave_data[startpoint+i]<thh_negative):
            wave_voiced_bi.append(1)
        else:
            wave_voiced_bi.append(0)
        #print(wave_data[i],wave_voiced_bi[i])
    print("Audio wave binary conversion finished")
    return(wave_voiced_bi)
            

    #fill some void points

def wave_binary_fill(wave_voiced_binary, point_range):
    #print('len_wavedata=', len(wave_voiced_binary))
    #print(len(wave_voiced_binary[1]))
    wave_binary_fill_result = []
    score = 0
    for i in range(len(wave_voiced_binary)):
        score = 0
        if (i< point_range):
            for j in range(i+point_range):
                score  = score + wave_voiced_binary[j]#/(i+point_range)
    
            if (score>= (i+point_range)/2):
                wave_binary_fill_result.append(score)
            else:
                wave_binary_fill_result.append(score)
        else:
            if(i<len(wave_voiced_binary)-point_range):
                for j in range(2*point_range):
                    score = score + wave_voiced_binary[i+j-point_range]#/(i+point_range)
                wave_binary_fill_result.append(score)
            else:
                for j in range(len(wave_voiced_binary)-i):
                    score = score+ wave_voiced_binary[len(wave_voiced_binary)-i+j]#/(i+point_range)
                wave_binary_fill_result.append(score)
        #print(score)
    print("Wave Binary Fill finished")
    return(wave_binary_fill_result)

def wave_binary_final(wave_binary_fill_result,score):
    wave_binary_final = []
    for i in range(len(wave_binary_fill_result)):
        if wave_binary_fill_result[i]>= score:
            wave_binary_final.append(1)
        else:
            wave_binary_final.append(0)
    return(wave_binary_final)        
    
def wave_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint, point_range, score,csv_folder_path):
    wave_voiced_binary = wave_convert_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint)
    wave_binary_fill_result = wave_binary_fill(wave_voiced_binary , point_range)
    wave_binary_final_result = wave_binary_final(wave_binary_fill_result,score)
    csv_table = np.transpose(wave_binary_final_result)
    with open('{}{}'.format(csv_folder_path,"Binary wav.csv"),"w", newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(csv_table)
    print("csv updated")
    f.close()
    return(wave_binary_final_result)
def picking_result(parameter_signal,csv_folder_path):
    startchannel = parameter_signal['start_channel'];
    endchannel = parameter_signal['end_channel'];
    upload_to_db = [[],[]]
    for channel_number in range(startchannel,endchannel+1):
        matrix = []
        circularshift_result_filepath =  '{}{}{}{}'.format(csv_folder_path,"circularshift_bandpower_channel_",channel_number,".csv")
        with open(circularshift_result_filepath,newline='') as channel1:
            reader = csv.reader(channel1)
            i=0
            for row in reader:
                if(i==0):
                   topic = row
                else:
                    if(i==1):
                        axis_name = row
                    else:
                        if(i==2):
                            column_name = row
                        else:
                            matrix.append(list(map(float, row))) 
                i = i+1
        channel1.close()
        #print(matrix)
        matrix_t = np.transpose(matrix).tolist()
        #print(matrix_t)
        max_r = sorted(matrix_t[2])[len(matrix_t[2])-1]
        #print("max_r = ", max_r)
        max_r_t_index=matrix_t[2].index(max_r)
        max_r_t = matrix_t[1][max_r_t_index]
        #print(max_r_t_index,max_r_t)
        upload_to_db[0].append(channel_number)
        upload_to_db[1].append(max_r_t)
        #print(upload_to_db)
    return(upload_to_db)


    
#run(cursor, sid, ECoG_filepath)

    
    
    
