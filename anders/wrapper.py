# requests subject name and populates subject table.
# requests initial file inputs from the user.

import psycopg2
import psycopg2.extras
import csv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from mod import config, Yannan, Jake, Joseph, David, Amy
try:
    import mod.mohammad.pac
except:
    pass

# request subject name from user.
name = input("Please enter subject name. ")

# connect to brain_db and establish cursor connection.
conn = psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

# query brain_db for existing subject name and select subject.
select_subject = """SELECT * from subjects WHERE name=%s"""
cursor.execute(select_subject, (name,))
subject_names = cursor.fetchall()


#### ACQUIRE SUBJECT NAME, EXPT TYPE, FILE INPUTS
if len(subject_names) == 0:
    # if subject name does not exist, request name, experiment type, and image paths.
    expt_type = input("Please enter experiment type (EEG/ECoG). ")
    # add a 'while' loop to demand only EEG or ECOG as input.
    
    # hard coded path to standard brain MR, standard brain SMR, standard EEG, blank CT.
    mr_path = "data/standard.nii"
    smr_path = "data/standard.cerebrum.mask.nii.gz"
    ct_path = ""
    eeg_coords = "data/EEG_10-20.csv"

    # acquire file paths based on experiment type and available images.
    if expt_type == "ECoG":
        mr = input("Do you have an MR file for this subject? (y/n) ")
        if mr == "y":
            mr_path = input("Please enter the MR file path: ")

        ct = input("Do you have a CT file for this subject? (y/n) ")
        if ct == "y":
            ct_path = input("Please enter the CT file path: ")
        else:
            ct_path = input("Please enter the file path with ECoG electrode coordinates: ")
    
    # insert subject data into subjects relation based on acquisitions from user.
    insert_subject = """INSERT INTO subjects(name,type,mr_path,ct_path) VALUES(%s,%s,%s,%s) RETURNING sid;"""
    cursor.execute(insert_subject, (name,expt_type,mr_path,ct_path))        
    # get subject ID
    sid = cursor.fetchone()["sid"]
    if ct_path and mr_path:
        Joseph.run(cursor, sid, ct_path, mr_path)

else:
    sid = subject_names[0]["sid"]
    expt_type = subject_names[0]["type"]
    mr_path = subject_names[0]["mr_path"]
    ct_path = subject_names[0]["ct_path"]
    
# commit the transaction to add content to subjects relation.
conn.commit()

### get existing signals
# SKULL STRIPPING
Yannan.run(cursor, sid, config.brainsuite_cortical_extraction_script, mr_path)
# need to feed output file path to "smr" column of subjects table
# outputs smr file path
# get coordinates from Joseph

# MR/CT ELECTRODE REGISTRATION
# if config.is_windows:
#    Jake.run(cursor, "test", "0", "100", "0", "100")
# Joseph.run(cursor, sid, ct_path, mr_path)
# output x, y, z coordinates to channel table
# talyrach coordinates (to be completed)

# Correct coordinates (Yannan - electrode_position_correction.py)
    # require smr file path as input
# electrode_position_correction.run(cursor, sid, smr_path)


#### ACQUIRE SIGNAL FILE PATHS
# request signal file paths and insert them into brain_db. 
cursor.execute("SELECT signal_path FROM signals where sid = %s", (sid, ))
existing_signals = [x["signal_path"] for x in cursor.fetchall()]
signals = []
new_signal_path = False
if len(existing_signals) == 0:
    new_signal_path = True
else:
    valid = False
    while not valid:
        print("You currently have the following existing signal files would you like to add another or use an existing?")
        print("\t0: (Add a new path)")
        for i in range(len(existing_signals)):
            print("\t%d: %s" % (i+1, existing_signals[i]))
        select_str = input("select an option ")
        try:
            select = int(select_str)
        except:
            continue
        if select == 0:
            new_signal_path = True
            valid = True
        elif select - 1 < len(existing_signals) and select - 1 > 0:
            new_signal_path = False
            valid = True
            signals.append(existing_signals[select-1])
if new_signal_path:
    signal = input("Please enter the first EEG or ECoG signal file path. ")
    signals.append(signal)
    insert_signals = """INSERT INTO signals(sid,signal_path) VALUES(%s,%s);"""
    for path in signals:
        cursor.execute(insert_signals, (sid,path))

# optional code in case we want to request multiple signal files.
# while signal != 'q':
#     # request another signal file path from the user.
#     signal = input("Please enter another signal file path, or enter 'q': ")
#
#     # add the signal file paths to the list.
#     if signal != 'q':
#         signals.append(signal)

# insert user-provided signal paths into signals table.

# commit the transaction to add content to signals relation.
conn.commit()

#### FILL CHANNEL TABLE WITH COORDINATES FROM EEG TABLE
if expt_type == "EEG":
    # hard coded path to EEG_channel_names.csv (from Box, converted from xlsx).
    with open('data/EEG_channel_names.csv') as subject_eeg:
        eeg_names = csv.reader(subject_eeg)
            
        select_eeg_channel = """SELECT * FROM eeg WHERE LOWER(eeg_name)=LOWER(%s);"""
        insert_eeg_channel = """INSERT INTO channels(sid, channel, eid) VALUES(%s,%s,%s);"""
        
        for row in eeg_names:
            eeg_coords = cursor.execute(select_eeg_channel, (row[1],))
            eeg_row = cursor.fetchall()[0]            
            cursor.execute(insert_eeg_channel, (sid, row[0],eeg_row[0]))

# commit the transaction to add content to channels table.
conn.commit()

#select_ecog_channel = """SELECT * FROM channels WHERE sid=%s;"""
#insert_ecog_channel = """INSERT INTO channels(sid, channel, x, y, z) VALUES(%s,%s,%s,%s,%s);"""
#for channel in channels:


#### SIGNAL ANALYSIS
# choose signal analysis method
# set up so you can choose multiple or only one to run
print("Enter the signal processing method that you would like to use.  Multiple can be entered (eg 23)")
print("\t(1) David")
print("\t(2) Amy")
print("\t(3) Band Power Over Time - Jake")
print("\t(4) Phase Amplitude Coupling - Mohammad")
method = input("Choice: ")

#### RUN INDIVIDUAL COMPONENT SCRIPTS

# MR/CT ELECTRODE REGISTRATION


#### SIGNAL ANALYSIS
# choose signal analysis method
# set up so you can choose multiple or only one to run
eeg_file = signals[0]
if '1' in method:
    David.run(cursor, sid, eeg_file)
if '2' in method:
    Amy.run(cursor, sid, eeg_file)
if '3' in method:
    method = 3
    startTime = input("Please enter the start time in seconds. ")
    stopTime = input("Please enter the stop time in seconds. ")
    interval = input("Please enter the number of intervals of this time range. ")
    startFrequency = input("Please enter the minimum frequency for the analysis. ")
    stopFrequency = input("Please enter the maximum frequency for the analysis. ")
    if config.is_windows:
        Jake.run(cursor, eeg_file, startTime, stopTime, interval, startFrequency, stopFrequency)
        # outputs .csv with scores for each time interval per channel

    with open('../data/jake.csv') as jakecsv:
        reader = csv.reader(jakecsv)
        for row in reader:
            columns = len(row)
    # insert scores into scores table from jakecsv
    insert_scores = """INSERT INTO scores(sid,channel,method,"""
    for i in range(columns):
        scores += "score{}".format(i)
    scores += """) VALUES(%s, %s, %s,"""+ ",".join(["%s" for _ in range(columns)]) + """);"""

    for row in reader:
        l = [sid, x + 1, method]
        l.extend(row)
        cursor.execute(insert_scores, l)


    # Jake has two methods: one for EDF and one for DAT
    # can specify time ranges and frequency bands of expt 

    # Jake signal processing: two methods (one for EDF and one for DAT)
    # can specify time ranges and frequency bands of expt
    # results in different scores (to be added as JakeMethod1a, JakeMethod1b)
    # method name might take format: "Jake_[time sequence]_[frequency band]"
    # will have to prompt user to specify their time ranges and frequency band

# Mohammad signal processing
# bandwidth (ranges)
    # low (1:40 Hz)
    # high (40:200 Hz)

# 3 signal numbers
    # number of signal channels to be processed
        # "enter 0 if you want all channels processed"
    # first signal channel
    # last signal channel
# 3 times (in minutes)
    # total time
        # "enter 0 if you want full range of time"
    # time window
    # time step

try:
    if '4' in method:
        band_lo = input("Please enter the desired low bandwidth range between 1 and 40 Hz (e.g. \"2, 14\"). ")
        band_hi = input("Please enter the desired low bandwidth range between 40 and 200 Hz (e.g. \"40, 200\"). ")
        ch_count = input("Please enter the number of signal channels you would like to process (enter 0 if you want all channels processed). ")
        ch_first = input("Please enter the number of the first signal channel to be processed. ")
        ch_last = input("Please enter the number of the last signal channel to be processed. ")
        sigtime_total = input("Please enter the total range of time (in minutes) you would like to process (enter 0 if you want to process entire range of time). ")
        sigtime_window = input("Please enter the short time window you would like to process (in minutes). ")
        sigtime_step = input("Please enter the short time step you would like to process (in minutes). ")
        mod.mohammad.pac.run(cursor, sid, eeg_file, band_lo, band_hi, ch_count,
                             ch_first, ch_last, sigtime_total, sigtime_window, sigtime_step)
except:
    pass

#### HEATMAP GENERATION
# Aaron.run

# close the cursor and database communication
cursor.close()
conn.close()

