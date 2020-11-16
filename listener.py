import RPi.GPIO as GPIO  ## Importing GPIO library
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
