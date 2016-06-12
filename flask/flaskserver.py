#!/usr/bin/env python

from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import json
import time
from datetime import datetime
import pickle

# flaskserver authentication
from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid or request is external
    """
    valid_pw = username == 'home' and password == '4343'
    return valid_pw

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        valid_ip = int(request.remote_addr.split('.')[-1]) != 1
        if not valid_ip:
            print "External request from %s, requesting authorization" % request.remote_addr
            auth = request.authorization
            auth_check = not auth or not check_auth(auth.username, auth.password)
            if auth_check:
                return authenticate()
        else:
            print "Internal request from %s, skipping authorization" % request.remote_addr
        return f(*args, **kwargs)
    return decorated

# setup the pin numbers associated with each button on the remote 
global switches
switches = {
    'Front': { 'on': 4, 'off': 17 },
    'Main': { 'on': 22, 'off': 18 },
    'Bedroom': { 'on': 23, 'off': 21 },
    'AC': { 'on': 24, 'off': 24 } # this is treated differently
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
@requires_auth
def index():
    sw_list = switches.keys()
    sw_list.remove('AC')

    try:
        data = pickle.load(open('tempdata.p','rb'))
    except EOFError:
        time.sleep(1)
        data = pickle.load(open('tempdata.p','rb'))

    hs_ts = ''
    for (time, temp) in zip(data['time'],data['temp']):
         hs_ts += '[Date.UTC(%4d,%2d,%2d,%2d,%2d,%2d), %.2f],' % ( time.year, time.month, time.day, time.hour, time.minute, time.second, temp )
    return render_template( 'index.html', switch_id=sw_list, current_t=data['temp'][-1], hs_timeseries=hs_ts )

# switch on/off page - json response to switching buttons on/off
@app.route('/switch/<string:id>/<string:mode>/')
@requires_auth
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

# switch the air conditioner on or off
@app.route('/switch/AC/<string:mode>/')
@requires_auth
def acswitch(mode):
    # error catching, mode must be on or off
    if mode not in ['off','on']:
        return json.dumps({'status': 1, 'message': 'Invalid mode specified', 'log': '' })

    # toggle the switch state
    if mode == 'on':
        GPIO.output(switches['AC'][mode],0)
        msg1 = "RPI GPIO - - [%s] BCM %d ON" % ( datetime.now().strftime('%d/%b/%Y %H:%M:%S'), switches['AC'][mode] )
        print "     " + msg1

    elif mode == 'off':
        GPIO.output(switches['AC'][mode],1)
        msg1 = "RPI GPIO - - [%s] BCM %d OFF" % ( datetime.now().strftime('%d/%b/%Y %H:%M:%S'), switches['AC'][mode] )
        print "     " + msg1
    return json.dumps({'status': 0, 'message': 'Air conditioner toggled %s' % mode, 'log': msg1 })

# execute application
if __name__ == '__main__':
    app.run(debug=True,host='192.168.1.70',port=5000)
