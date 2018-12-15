def find_index_by_time(time_list, starttime, endtime):
#    print(starttime)
#    print(endtime)
    if(starttime<time_list[0]):
        starttime_in_table = time_list[0]
    else:
        starttime_in_table = ((starttime-time_list[0])//(time_list[1]-time_list[0]))*(time_list[1]-time_list[0])+time_list[0]
#        print("time_step=",time_list[1]-time_list[0])
#        print()
    if(endtime>time_list[len(time_list)-1]):
        endtime_in_table = time_list[len(time_list)-1]
    else:
        endtime_in_table = ((endtime-time_list[0])//(time_list[1]-time_list[0]))*(time_list[1]-time_list[0])+time_list[0]
    startpoint = time_list.index(starttime_in_table)
    endpoint = time_list.index(endtime_in_table)
    return_dict = {'startpoint':startpoint,'endpoint':endpoint}
    return(return_dict)


'''
point = find_index_by_time([7,10,13,16,19],6,18)
print(point)
'''
