#!/usr/bin/env python
#----------------------------------------------------
# scrape_pitchfx.py
#
# python code to grab pitch fx data from online xml
# converts data to local sql database
#----------------------------------------------------


#----------------------------------------------------
# imports and aliases
#----------------------------------------------------
import sys
import os
import re
import sqlite3
import load_pitchfx_mod as pm


#----------------------------------------------------
# kernel
#----------------------------------------------------
# check number of arguments
if len(sys.argv) < 5:
    print "Usage:"
    print "    %s [begin date] [end date] [name of db] [prompt?]" %(sys.argv[0])
    print " data format: mm-dd-yyyy"
    sys.exit()

# grab variables
bdate = sys.argv[1]
edate = sys.argv[2]
dbname = sys.argv[3]
prompt = bool(sys.argv[4])

# parse beginning and end dates
date = re.compile("^(\d\d)-(\d\d)-(\d\d\d\d)$")                                 
find = date.search(bdate)                                                       
if (find):                                                                      
    bmonth = find.group(1)
    bday = find.group(2)
    byear = find.group(3)
else:                                                                           
    print "Start date format does not work"
    sys.exit()
bdate = int('%s%s%s' %(byear, bmonth, bday))                                      
find = date.search(edate)                                                       
if find:                                                                      
    emonth = find.group(1)
    eday = find.group(2)
    eyear = find.group(3)
else:                                                                           
    print "End date format does not work"
    sys.exit()
edate = int('%s%s%s' %(eyear, emonth, eday))                                      
# check that dates make sense                                                   
if edate < bdate:                                                             
    print "Need begin date to be earlier than end date"
    sys.exit()

# touch sqlite3 database
if os.path.isfile(dbname) is False:
   db = sqlite3.connect(dbname)
   hdb = db.cursor()
   pm.pitchfx_init(hdb)
else:
   db = sqlite3.connect(dbname)
   hdb = db.cursor()
  

# add information to database
pm.pitchfx_add(db, hdb, bdate, edate, prompt)

# clean up
db.commit()
hdb.close()
db.close()
