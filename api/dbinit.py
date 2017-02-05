#!/usr/bin/python3.5
#-*- coding:utf_8 -*-
import sqlite3
dbname = 'database.db'
connection = sqlite3.connect(dbname)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE group (
                                group_id text,
                                step integer,
                                gole text,
                                station text,
                                spot text,
                                meetingtime integer,
                                station1 text,
                                station2 text,
                                station3 text,
                                station4 text,
                                station5 text,
                                stationendtime integer,
                                station1count integer,
                                station2count integer,
                                station3count integer,
                                station4count integer,
                                station5count integer,
                                spot1 text,
                                spot2 text,
                                spot3 text,
                                spot4 text,
                                spot5 text,
                                spotendtime integer,
                                spot1count integer,
                                spot2count integer,
                                spot3count integer,
                                spot4count integer,
                                spot5count integer,
                                );''')

cursor.close()
