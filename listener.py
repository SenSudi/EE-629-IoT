import RPi.GPIO as GPIO  ## Import GPIO library
import socket
import csv

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup('port_example_33', GPIO.OUT)
GPIO.setup('port_example_11', GPIO.OUT)

GPIO.setup('port_example_13', GPIO.OUT)
GPIO.setup('port_example_15', GPIO.OUT)

GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)

GPIO.output(29, True)
GPIO.output(31, True)

UDP_IP = "0.0.0.0"
UDP_PORT = 5050

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    raw = data
    # print raw
    limited = raw.split(",")
    x = float(limited[3])
    y = float(limited[4])
    # print int(x), int(y)

    if int(x) >= 3 and -3 < int(y) < 3:
        print
        "FORWARD"
        GPIO.output(33, True)
        GPIO.output(11, False)
        GPIO.output(13, True)
        GPIO.output(15, False)

    elif int(x) <= -3 and -3 < int(y) < 3:
        print
        "BACKWARD"
        GPIO.output(33, False)
        GPIO.output(11, True)
        GPIO.output(13, False)
        GPIO.output(15, True)

    elif int(y) >= 3 and -3 < int(x) < 3:
        print
        "LEFT"
        GPIO.output(33, False)
        GPIO.output(11, True)
        GPIO.output(13, True)
        GPIO.output(15, False)

    elif int(y) <= -3 and -3 < int(x) < 3:
        print
        "RIGHT"
        GPIO.output(33, True)
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, True)


    else:
        print
        "STOP"
        GPIO.output(33, False)
        GPIO.output(11, False)
        GPIO.output(13, False)
        GPIO.output(15, False)