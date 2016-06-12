#!/usr/bin/env python

from flask import Flask, render_template
import RPi.GPIO as GPIO
import json
import time
from datetime import datetime

# 

# setup the pin numbers associated with each button on the remote 
global switches
switches = {
    'Front': { 'on': 4, 'off': 17 },
    'Main': { 'on': 22, 'off': 18 },
    'Bedroom': { 'on': 23, 'off': 21 },
}

# setup channels to be outputs
GPIO.setmode(GPIO.BCM)
for key, val in switches.iteritems():
    GPIO.setup(val['on'], GPIO.OUT)
    GPIO.setup(val['off'], GPIO.OUT)

# flask web application initialization
app = Flask(__name__)

# index page - a simple page with buttons to turn on/off switches
@app.route('/')
def index():
    return render_template( 'index.html', switch_id=switches.keys() )

# switch on/off page - json response to switching buttons on/off
@app.route('/switch/<string:id>/<string:mode>/')
def switch(id,mode):
    # error catching, mode must be on or off
    if mode not in ['off','on']:
        return json.dumps({'status': 1, 'message': 'Invalid mode specified', 'log': '' })
    
    # error catching, switch ID must be in the switches dict
    if id not in switches.keys():
        return json.dumps({'status': 1, 'message': 'Invalid switch ID', 'log': '' })

    # we can now proceed with toggling the switch
    msg1 = "RPI GPIO - - [%s] BCM %d ON" % ( datetime.now().strftime('%d/%b/%Y %H:%M:%S'), switches[id][mode] )
    print "     " + msg1
    GPIO.output(switches[id][mode], 1)

    time.sleep(0.25)

    msg2 = "RPI GPIO - - [%s] BCM %d OFF" % ( datetime.now().strftime('%d/%b/%Y %H:%M:%S'), switches[id][mode] )
    print "     " + msg2
    GPIO.output(switches[id][mode], 0)

    return json.dumps({'status': 0, 'message': 'Switch %s toggled %s' % (str(id), mode), 'log': '%s<br>%s' % (msg1, msg2) })

# execute application
if __name__ == '__main__':
    app.run(debug=True,host='192.168.1.70',port=5000)
