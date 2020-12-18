
# Android Accelerometer controlled surveillance robot using Raspberry Pi 4

### Final project for the class CPE 629 IoT.

### Aim: To create a vehicle controlled by Raspberry Pi, based on input from an Android phone's gyroscope.

### Purpose: For surveillance of unknown or treacherous territory.

### Material Utilized:

1. Raspberry Pi 4B
2. Raspberry Pi transparent plastic case and Cooling Fan
3. L298N H-Bridge motor-controller drive.
4. Connecting Wires (Jumper Cable) and screws
5. Mini-Breadboard
6. 9V Batteries (X2)
7. SDP sensor App (for sending signals to Android phone)
8. Wheels (X4) 
9. Chassis (X2)
10. DC Gearbox Motor TT 200RPM  (X4)

### Getting Started:

1. In order to get started, we must first run the listener.py code within Raspberry Pi.
2. Next, we should download the Sesor UDP application on the android system, in order to send changes in the gyroscope to the Raspberry Pi.
3. Once the program is responsive to changes in the gyroscope, we should initiate the harware setup
4. For setting up the vehicle, we shall connect the wheels to the motors and fix them in place on the chassis.
5. Next, we must provide control using the L298N controller. For doing that, we should attach the negative terminal of the 9V battery to the GND and the positive terminal to the 12V terminal on the controller. Once , a red light glows, output terminals are provided to the terminals of the motors to be controlled. Note: The even outpput ]
6. Next input terminals of the controller is connected to the GPIO pins of Raspberry Pi.
7. A connection is given from the Ground Terminal of Raspberry Pi to the GND terminal on the controller (to which the negative terminal of the battery is provided).
8. Once proper connection is established, the motors should respond to changees in the gyroscope readings

<a href="https://youtu.be/gnP4VA49ppM"><img src="http://img.youtube.com/vi/<gnP4VA49ppM>/default.jpg" 
alt="Video Showing Gyroscope Control of Vehicle" width="240" height="180" border="10" /></a>
