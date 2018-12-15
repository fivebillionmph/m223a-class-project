'''
brain_sweet.py
BRAINSWEET FILE I/O AND DATABASE INTEGRATION
'''

import os
import csv
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from mod import config, util, Yannan, Jake, Joseph, David, Amy, electrode_position_correction, Aaron, james, audio_analysis
try:
    from mod.convert_dat_to_csv import convert_dat_to_csv
except:
    pass

try:
    from mod.mohammad import pac
except:
    pass

'''
ESTABLISH DATABASE CONNECTION
'''
# connect to brain_db and establish cursor connection.
conn = psycopg2.connect(dbname='brain_db', user='postgres', password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# constants
MNI_MASK_FILE = "data/MNI_mask_template.nii.gz"

'''
ACQUIRE SUBJECT NAME, EXPT TYPE, FILE INPUTS
'''
# request subject name from user.
name = input("Please enter subject name. ")

# query brain_db for existing subject name and select subject.
select_subject = """SELECT * FROM subjects WHERE name=%s"""
cursor.execute(select_subject, (name,))
subject_names = cursor.fetchall()

if len(subject_names) == 0:
    # if subject name does not exist, request name, experiment type, and image paths.
    while True:
        expt_type = input("Please enter experiment type (EEG/ECoG). ")
        if expt_type in ["EEG", "ECoG"]:
            break
        print("Invalid experiment type")

    # hard coded path to standard brain MR, standard brain SMR, blank CT.
    mr_path = "data/standard.nii"
    smr_path = "data/standard.cerebrum.mask.nii.gz"
    ct_path = ""

    # acquire file paths based on experiment type and available images.
    if expt_type == "ECoG":
        mr = input("Do you have an MR file for this subject? (y/n) ")
        if mr == "y":
            mr_path = util.inputFilepath("Please enter the MR file path: ")

        ct = input("Do you have a CT file for this subject? (y/n) ")
        if ct == "y":
            ct_path = util.inputFilepath("Please enter the CT file path: ")
        else:
            ct_path = util.inputFilepath("Please enter the file path with ECoG electrode coordinates: ")

    # insert subject data into subjects relation based on acquisitions from user.
    insert_subject = "INSERT INTO subjects(name,type,mr_path,ct_path,smr_path) VALUES(%s,%s,%s,%s,%s) RETURNING sid;"
    cursor.execute(insert_subject, (name, expt_type, mr_path, ct_path, smr_path))
    # get subject ID
    sid = cursor.fetchone()["sid"]

    if expt_type == "ECoG" and mr == "y":
        # SKULL STRIPPING
        Yannan.run(cursor, sid, config.brainsuite_cortical_extraction_script, mr_path)
        # need to feed output file path to "smr" column of subjects table
        # outputs smr file path (standard.cerebrum.mask.nii)
        # TO DO: have rest of the script pick up after 2 minutes, or when desired file is detected

    '''
    MR/CT ELECTRODE REGISTRATION

    1. CT/MR ECoG registration (Joseph)
    2. Talairach ECoG registration (Joseph)
        ECoG, don't have CT or MR, need to use Talairach
        read standard Talairach brain (MNI_MASK_FILE)
        then goes to web to convert to another format called MNI
        then plot that on standard brain
        # output x, y, z coordinates to channel table
        # talairach coordinates (to be completed)
    3. Coordinate Correction (Yannan)
        # Yannan - electrode_position_correction.py
        # require smr file path as input
    '''

    cursor.execute("SELECT smr_path FROM subjects WHERE sid = %s", (sid,))
    smr_path = cursor.fetchone()["smr_path"]
    if ct_path and mr_path:
        electrode_data = Joseph.run(cursor, sid, ct_path, mr_path)
        electrode_position_correction.run(cursor, sid, smr_path, electrode_data)
    elif not mr_path and not ct_path:
        # Talairach ECoG registration (part 2)
        electrode_data = register_talairach.run(cursor, sid)
        electrode_position_correction.run(cursor, sid, MNI_MASK_FILE, electrode_data)

else:
    sid = subject_names[0]["sid"]
    expt_type = subject_names[0]["type"]
    mr_path = subject_names[0]["mr_path"]
    ct_path = subject_names[0]["ct_path"]

# commit the transaction to add content to subjects relation.
conn.commit()

# FILL CHANNEL TABLE WITH COORDINATES FROM EEG TABLE
# TO DO: setup so it UPDATES instead of INSERTS if that SID already has channel coordinates
if expt_type == "EEG":
    # hard coded path to EEG_channel_names.csv (from Box, converted from xlsx).
    eeg_channel_names = "data/EEG_channel_names.csv"
    eeg_channels = input("Do you have a subject-specific EEG channel file for this subject? (y/n) ")
    if eeg_channels == "y":
        eeg_channel_names = util.inputFilepath("Please enter the subject-specific EEG channel names file path: ")
    with open(eeg_channel_names) as subject_eeg:
        eeg_names = csv.reader(subject_eeg)
        select_eeg_channel = """SELECT * FROM eeg WHERE LOWER(eeg_name)=LOWER(%s);"""
        insert_eeg_channel = """INSERT INTO channels(sid, channel, eid) VALUES(%s,%s,%s);"""

        for row in eeg_names:
            eeg_coords = cursor.execute(select_eeg_channel, (row[1],))
            eeg_row = cursor.fetchall()[0]
            cursor.execute(insert_eeg_channel, (sid, row[0], eeg_row[0]))

# commit the transaction to add content to channels table.
conn.commit()


''' 
ACQUIRE SIGNAL FILE PATHS

'''
# request signal file paths and insert them into brain_db. 
cursor.execute("SELECT signal_path FROM signals WHERE sid = %s", (sid,))
existing_signals = [x["signal_path"] for x in cursor.fetchall()]
signals = []
new_signal_path = False
if len(existing_signals) == 0:
    new_signal_path = True
else:
    valid = False
    while not valid:
        print("You currently have the following existing signal files available for this subject; "
              "would you like to add another, or use an existing file?")
        print("\t0: (Add a new path)")
        for i in range(len(existing_signals)):
            print("\t%d: %s" % (i + 1, existing_signals[i]))
        select_str = input("select an option ")
        try:
            select = int(select_str)
        except:
            continue
        if select == 0:
            new_signal_path = True
            valid = True
        # elif len(existing_signals) > select - 1 >= 0:
        elif select - 1 < len(existing_signals) and select - 1 >= 0:
            new_signal_path = False
            valid = True
            signals.append(existing_signals[select - 1])
if new_signal_path:
    signal = input("Please enter the signal file path. ")
    signals.append(signal)
    # insert user-provided signal paths into signals table.
    insert_signals = """INSERT INTO signals(sid,signal_path) VALUES(%s,%s);"""
    for path in signals:
        cursor.execute(insert_signals, (sid, path))

# commit the transaction to add content to signals relation.
conn.commit()

'''
SIGNAL ANALYSIS
'''
# choose signal analysis method
sig_file = signals[0]
print("Enter the signal processing method that you would like to use.  Multiple can be entered (eg 23)")
print("\t(1) Channel Scoring (David)")
print("\t(2) Channel Quality Control (Amy)")
print("\t(3) Band Power Over Time (Jake)")
print("\t(4) Phase Amplitude Coupling (Mohammad)")
print("\t(5) Audio Analysis (Ge)")
method = input("Choice: ")

if '1' in method:
    sig_file_csv = convert_dat_to_csv.run(sig_file)
    David.run(cursor, sid, sig_file_csv)
if '2' in method:
    Amy.run(cursor, sid, sig_file_csv)
if '3' in method:
    try:
        method = 3
        x = 0
        startTime = input("Please enter the start time in seconds. ")
        stopTime = input("Please enter the stop time in seconds. ")
        interval = input("Please enter the number of intervals of this time range. ")
        startFrequency = input("Please enter the minimum frequency for the analysis. ")
        stopFrequency = input("Please enter the maximum frequency for the analysis. ")
        if config.is_windows:
            Jake.run(cursor, sig_file, startTime, stopTime, interval, startFrequency, stopFrequency)
            # outputs .csv with scores for each time interval per channel
            # file will have same name as input file, with "-3.csv" extension

        with open(sig_file + '-3.csv') as jakecsv:
            reader = csv.reader(jakecsv)
            for row in reader:
                columns = len(row)

        # insert scores into scores table from jakecsv
        insert_scores = """INSERT INTO scores(sid,channel,method"""
        for i in range(columns):
            insert_scores += ",score{}".format(i)
        insert_scores += """) VALUES(%s, %s, %s,""" + ",".join(["%s" for _ in range(columns)]) + """);"""

        for row in reader:
            x += 1
            l = [sid, x, method]
            l.extend(row)
            cursor.execute(insert_scores, l)
    except Exception as e:
        print(e)

    # Jake signal processing: two methods (one for EDF and one for DAT)
    # can specify time ranges and frequency bands of expt
    # results in different scores (to be added as methods 3a and 3b, perhaps?)

if '4' in method:
    try:
        method = 4
        x = 0
        band_lo = input("Please enter the desired low bandwidth range between 1 and 40 Hz (e.g. \"2 14\"). ")
        band_lo = [float(i) for i in band_lo.split()]
        band_hi = input("Please enter the desired low bandwidth range between 40 and 200 Hz (e.g. \"40 200\"). ")
        band_hi = [float(i) for i in band_hi.split()]
        ch_count = float(
            input("Please enter the number of signal channels you would like to process (enter 0 if you want to "
                  "process all channels). "))
        ch_first = float(input("Please enter the number of the first signal channel to be processed. "))
        ch_last = float(input("Please enter the number of the last signal channel to be processed. "))
        sigtime_total = float(
            input("Please enter the total range of time (in minutes) you would like to process (enter 0 if "
                  "you want to process entire range of time). "))
        sigtime_window = float(input("Please enter the short time window you would like to process (in minutes). "))
        sigtime_step = float(input("Please enter the short time step you would like to process (in minutes). "))
        pac.run(sig_file, band_lo, band_hi, ch_count, ch_first, ch_last, sigtime_total, sigtime_window, sigtime_step)

        with open(sig_file + '-4.csv') as mocsv:
            reader = csv.reader(mocsv)
            for row in reader:
                columns = len(row)

        # insert scores into scores table from mocsv
        insert_scores = """INSERT INTO scores(sid,channel,method"""
        for i in range(columns):
            insert_scores += ",score{}".format(i)
        insert_scores += """) VALUES(%s, %s, %s,""" + ",".join(["%s" for _ in range(columns)]) + """);"""

        for row in reader:
            x += 1
            l = [sid, x, method]
            l.extend(row)
            cursor.execute(insert_scores, l)

    except Exception as e:
        print(e)

'''
Audio Analysis (Ge Fang)
'''
if '5' in method:
    try:
        method = 5
        audio_analysis.run(cursor, sid, sig_file)
    except Exception as e:
        print(e)

# commit score additions to database
conn.commit()

james.run(cursor, sid)

'''
HEATMAP GENERATION
    how do we deal with multiple scoring methods?
    multiple interfaces to pop up?
    show each output sequentially?
    ask user which one they want to view?
'''
Aaron.run(cursor, sid)

# close the cursor and database communication
cursor.close()
conn.close()
