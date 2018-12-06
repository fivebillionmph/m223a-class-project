'''
import importlib
import sys 
import os
import matplotlib.pyplot as plt
from read_wave_to_list import *
sys.path.append(os.path.abspath("C:\\Users\dell\\Desktop\\FALL2018\\223A\\Project"))

'''
def wave_convert_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint):
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
    
def wave_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint, point_range, score):
    wave_voiced_binary = wave_convert_binary(wave_data,thh_positive,thh_negative,startpoint,endpoint)
    wave_binary_fill_result = wave_binary_fill(wave_voiced_binary , point_range)
    wave_binary_final_result = wave_binary_final(wave_binary_fill_result,score)
    return(wave_binary_final_result)
'''
#testbench    

wave_file = "audio1.wav"
wave_data = read_wave_to_list(wave_file)
thh_positive = [500,550,600]
thh_negative = [-500,-550,-600]
startpoint= 15000
endpoint = 100000
point_range = [500,1000,1500]
score = [400,500,600]
wave_final_result = wave_binary(wave_data,thh_positive[1],thh_negative[1],startpoint,endpoint, point_range[1], score[1])
#wave_voiced_binary_1 = wave_convert_binary(wave_data,thh_positive[1],thh_negative[1],startpoint,endpoint)
#wave_binary_fill_result_1 = wave_binary_fill(wave_voiced_binary_1 , point_range[1])
#wave_binary_final_1 = wave_binary_final(wave_binary_fill_result_1,score[0])
#wave_voiced_binary_2 = wave_convert_binary(wave_data,thh_positive[1],thh_negative[1],startpoint,endpoint)
#wave_binary_fill_result_2 = wave_binary_fill(wave_voiced_binary_2 , point_range[1])
#wave_binary_final_2 = wave_binary_final(wave_binary_fill_result_2,score[1])
#wave_voiced_binary_3 = wave_convert_binary(wave_data,thh_positive[1],thh_negative[1],startpoint,endpoint)
#wave_binary_fill_result_3 = wave_binary_fill(wave_voiced_binary_3 , point_range[1])
#wave_binary_final_3 = wave_binary_final(wave_binary_fill_result_3,score[2])
pl.subplot(211)
pl.plot(np.arange(startpoint,endpoint,1),wave_data[startpoint:endpoint])
pl.subplot(212)
pl.plot(np.arange(startpoint,endpoint,1),wave_final_result)
pl.show()
'''
'''
pl.subplot(431)
plt.gca().set_title('Original Signal')
pl.plot(np.arange(0,len(wave_data),1),wave_data)
pl.subplot(433)
plt.gca().set_title('A Portion of Original Signal')
#pl.plot(np.arange(0,len(wave_data),1),wave_data )
pl.plot(np.arange(startpoint,endpoint,1),wave_data[startpoint:endpoint])
pl.subplot(434)
plt.gca().set_title('First Bi-Conv. with tth 550')
pl.plot(np.arange(startpoint,endpoint,1),wave_voiced_binary_1)
pl.subplot(435)
plt.gca().set_title('Window Score. with width 1000')
pl.plot(np.arange(startpoint,endpoint,1),wave_binary_fill_result_1)
pl.plot(np.arange(startpoint,endpoint,1),np.arange(startpoint,endpoint,1)*0+point_range[1]*0.4)
pl.plot(np.arange(startpoint,endpoint,1),np.arange(startpoint,endpoint,1)*0+point_range[1]*0.5)
pl.subplot(436)
plt.gca().set_title('Second Bi-Conv with Score 400')
pl.plot(np.arange(startpoint,endpoint,1),wave_binary_final_1)

pl.subplot(437)
#plt.gca().set_title('First Bi-Conv. with tth 550')
pl.plot(np.arange(startpoint,endpoint,1),wave_voiced_binary_2)
pl.subplot(438)
#plt.gca().set_title('Window Score. with width 1000')
pl.plot(np.arange(startpoint,endpoint,1),wave_binary_fill_result_2)
pl.plot(np.arange(startpoint,endpoint,1),np.arange(startpoint,endpoint,1)*0+point_range[1]*0.4)
pl.plot(np.arange(startpoint,endpoint,1),np.arange(startpoint,endpoint,1)*0+point_range[1]*0.5)
pl.subplot(439)
plt.gca().set_title('Second Bi-Conv with Score 500')
pl.plot(np.arange(startpoint,endpoint,1),wave_binary_final_2)
pl.subplot(4,3,10)
#plt.gca().set_title('First Bi-Conv. with tth 600')
pl.plot(np.arange(startpoint,endpoint,1),wave_voiced_binary_3)
pl.subplot(4,3,11)
#plt.gca().set_title('Window Score. with width 1500')
pl.plot(np.arange(startpoint,endpoint,1),wave_binary_fill_result_3)
pl.plot(np.arange(startpoint,endpoint,1),np.arange(startpoint,endpoint,1)*0+point_range[1]*0.4)
pl.plot(np.arange(startpoint,endpoint,1),np.arange(startpoint,endpoint,1)*0+point_range[1]*0.5)
pl.subplot(4,3,12)
plt.gca().set_title('Second Bi-Conv with Score 500')
pl.plot(np.arange(startpoint,endpoint,1),wave_binary_final_3)

#pl.subplot(313)
#pl.plot(np.arange(0,len(wave_binary_fill_result),1),wave_binary_fill_result )
'''
#pl.show()
            

