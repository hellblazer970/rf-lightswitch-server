#!/usr/bin/python

import Adafruit_MCP9808.MCP9808 as MCP9808
import time
from datetime import datetime
import pickle

# init pickle db
# >>> data={'time':[],'temp':[]} 
# >>> pickle.dump(data,open('temperatures.p','wb'))

sensor = MCP9808.MCP9808()

n_samples = 10
tempavg = 0.0
for i in range(n_samples):
    temp = sensor.readTempC()*9.0/5.0 + 32.0
    tempavg = tempavg + temp/float(n_samples)
    time.sleep(0.1)

now = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')

datafile = '/home/pi/webserver/tempdata.p'
data = pickle.load(open( datafile ))
data['time'].append(now)
data['temp'].append(tempavg)
data['time'] = data['time'][-1440:]
data['temp'] = data['temp'][-1440:]
print data

pickle.dump(data, open( datafile ,'wb')) 
