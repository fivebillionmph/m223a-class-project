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


#import matlab.engine
#import pylab
#method = 5
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
            
def csv_to_db_function(csv_file_path):
    return_table = [[],[]]
    with open(csv_file_path,newline = '') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            return_table[0].append(int(row[0]))
            return_table[1].append(float(row[1]))
    f.close()
    return(return_table)
        

def run(cursor, sid, ECoG_filepath):
    method = 5
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
    cmd = int(str(input("input '0' for getting ECOG path, input '1'for uploading scores to database:")))
    if (cmd == 0):
        with open('{}{}{}{}'.format(csv_folder_path,"ECoG_path_SID_",sid,".txt"), "w") as f:
            f.write("SID"+"\n")
            f.write(str(sid)+"\n")
            f.write("ECOG FILE PATH"+"\n")
            f.write(ECoG_filepath+"\n")
            f.closed
        print("txt tile generated")
    else:
        if(cmd ==1):
            upload_path = (str(input("input the absolute path of score file you wish to upload,please use '\\\' instead of '\\'")))
            csv_to_db = csv_to_db_function(upload_path)
            for i in range(len(csv_to_db[0])):
                insert_scores = "INSERT INTO scores(sid,channel,method,score0) VALUES(%s, %s, %s, %s);"
                cursor.execute(insert_scores, (sid, csv_to_db[0][i], method, csv_to_db[1][i]))
            print("data has been uploaded to database")
        else:
            print("wrong command")
  

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print("folder created:",directory)
        else:
            print("folder existed:",directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)





    
#run(cursor, sid, ECoG_filepath)

