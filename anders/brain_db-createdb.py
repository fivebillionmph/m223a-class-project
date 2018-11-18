# create database brain_db 
# run on installation (only once)

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn=psycopg2.connect(user='postgres',password='pass')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor=conn.cursor()

# drop brain_db database if exists and recreate
cursor.execute('DROP DATABASE IF EXISTS brain_db')
cursor.execute('CREATE DATABASE brain_db')

# grant all permissions to user postgres
cursor.execute('GRANT ALL ON DATABASE brain_db TO postgres')
cursor.execute('GRANT ALL ON DATABASE brain_db TO public')

# commit the transaction
conn.commit()
# close the database communication
cursor.close()