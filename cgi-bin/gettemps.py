#!/usr/bin/python

import pickle
import time, datetime

# location of file with pickle data for temperature
filename = '/home/pi/webserver/tempdata.p'

# load the file. try twice in the event it is being written to now
try:
    data = pickle.load(open(filename,'rb'))
except EOFError:
    time.sleep(1)
    data = pickle.load(open(filename,'rb'))

# convert to datetime series. 
# json module is too slow on RPi so we'll do it manually
tjson = []
for (dt,temp) in zip(data['time'],data['temp']):
    tjson.append("[%i,%.2f]" % (int(time.mktime(dt.timetuple()))*1000, temp) )
# return json series
print "Content-type: application/json"
print ""
print '{"series":[' + ','.join(tjson) + ']}'
