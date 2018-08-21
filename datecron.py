import sys
import os
from datetime import timedelta
import datetime

target = open('/home/file.txt','a')
target.truncate()
date=datetime.datetime.now()
target.write("hello at %s\n"%(str(date)))
target.close()

#In order to make it executable, you need to change the permissions. Use the following command to make it executable: 
#sudo chmod +x datecron.py
#or sudo chmod 755 datecron.py

#In terminal
#sudo crontab -e
#at the end 
#For evry minute
#*/1 * * * * /usr/bin/python2 /home/cso/Desktop/script/datecron.py >>/home/cso/Desktop/script/datecron.txt 2>&1


#10:00 Am every day
#0 10 * * * /usr/bin/python2 /home/cso/Desktop/script/auto_neo_to_sql_new_with_crosscheck.py >> /home/cso/Desktop/script/neo4jscript.txt 2>&1

#https://crontab.guru/#0_10_*_5_2-6

