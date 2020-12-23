
''' 
    Author: Sudipto Sen
    Date Created: 12.02.2020
'''

import RPi.GPIO as GPIO ## Import GPIO library
import socket
import csv

GPIO.setwarnings(GPIO.LOW)

in1 = 33
in2 = 35
in3 = 37
in4 = 39
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.sta

UDP_IP = "0.0.0.0"
UDP_PORT = 5050

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while GPIO.HIGH:
    data, addr = sock.recvfrom(1024)
    raw=data
    #print raw
    limited=raw.split(",")
    x=float(limited[3])
    y=float(limited[4])
    #print int(x), int(y)

    if int(x) >= 3 and -3<int(y)<3:
       print "FORWARD"
       GPIO.output(in1,GPIO.HIGH)
       GPIO.output(in2,GPIO.LOW)
       GPIO.output(in3,GPIO.HIGH)
       GPIO.output(in4,GPIO.LOW)
	
    elif int(x) <= -3  and -3<int(y)<3:
       print "BACKWARD"
       GPIO.output(in1,GPIO.LOW)
       GPIO.output(in2,GPIO.HIGH)
       GPIO.output(in3,GPIO.LOW)
       GPIO.output(in4,GPIO.HIGH)

    elif int(y) >= 3 and -3<int(x)<3:
        print "LEFT"
	      GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)

    elif int(y) <= -3 and -3<int(x)<3:
        print "RIGHT"
	      GPIO.output(33,GPIO.LOW)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        GPIO.output(15,GPIO.LOW)


    else:
        print "STOP"
        GPIO.output(33,GPIO.LOW)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(13,GPIO.LOW)
        GPIO.output(15,GPIO.LOW)
