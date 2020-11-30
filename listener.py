import RPi.GPIO as GPIO  ## Importing GPIO library
# import socket
# import csv
# Front left tire => GPIO 17 (pin 12)
# Front right tire => GPIO 18
# Back left tire => GPIO 26
# Back right tire => GPIO 20

import Rpi.GPIO as GPIO
# import socket
# import csv

#GPIO.setwarnings
from gpiozero import motor

motor = Motor(18,17)
motor.forward()

GPIO.setmode(GPIO.BOARD)  # also tried GPIO.BCM

GPIO.setup(18,GPIO.OUT)

while True:
	print ("Forward")
	GPIO.output(18,True)
