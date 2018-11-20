# establish database schema
# run on installation (only once)

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn=psycopg2.connect(dbname='brain_db',user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor()

# create 5 tables: subjects, signals, channels, scores, eeg
# create "subjects" table to house imaging file paths
subjects="""CREATE TABLE subjects(
        sid serial primary key,         
        name varchar(255) not null,     
        type varchar(255) not null,     
        ct_path varchar(255),           
        mr_path varchar(255),           
        rct_path varchar(255),          
        smr_path varchar(255))"""       
cursor.execute(subjects)

# create "signals" table to house signal file paths
signals="""CREATE TABLE signals(
        sid integer not null,
        signal_path varchar(255) not null,
        foreign key (sid)
            references subjects (sid)
            on update cascade on delete cascade)"""
cursor.execute(signals)

# create "eeg" table to house eeg channel names and coordinates
# this data will be hard-coded (does not change across subjects)
eeg="""CREATE TABLE eeg(
        eid integer primary key,
        eeg_name varchar(3) not null,
        x integer,
        y integer,
        z integer)"""
cursor.execute(eeg)

# create "channels" table to house ecog channel coordinates
channels="""CREATE TABLE channels(
        sid integer not null,
        channel integer not null,
        eid integer,
        x integer,
        y integer,
        z integer,
        CONSTRAINT channels_eid_fkey FOREIGN KEY (eid)
            REFERENCES public.eeg (eid) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT channels_sid_fkey FOREIGN KEY (sid)
            REFERENCES public.subjects (sid) MATCH SIMPLE
            ON UPDATE CASCADE ON DELETE CASCADE)"""
cursor.execute(channels)

# create "scores" table to house scores, based on method used
scores="""CREATE TABLE scores(
        sid integer not null,
        channel integer not null,
        method varchar(255) not null,
        score numeric,
        foreign key (sid)
            references subjects (sid)
            on update cascade on delete cascade)"""
cursor.execute(scores)

# commit the transaction
conn.commit()
# close the database communication
cursor.close()