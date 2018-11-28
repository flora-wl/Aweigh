# This script outputs latitude to the console from polarisation analyser readings

import time
import math
import py_qmc5883l
import Adafruit_ADS1x15
import RPi.GPIO as GPIO
import numpy

# Servo motor
servoPIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT) #Servo pin 18
p = GPIO.PWM(18, 50) #Frequency is 50Hz
p.start(5) #Duty cycle is 5 to turn 60 degrees

# Magnetometer initialisation
sensor = py_qmc5883l.QMC5883L()
m = sensor.get_magnet()

# ADC polarisation analyser readings.
adc = Adafruit_ADS1x15.ADS1115()
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1
# Array for first reading
s1_array = [0,0,0,0,0,0,0,0,0,0]
# Array for second reading
s2_array = [0,0,0,0,0,0,0,0,0,0]

# Define end time
t_end = time.time() + 2

# Run program once for fixed amount of time
while time.time() < t_end:

# Take two sensor readings
    #First reading
    for i in range(0,10,1):
        s1_array[i]=adc.read_adc(i, gain=GAIN)
        s1 = max(s1_array)
    # Turn motor 60 degrees
    p.ChangeDutyCycle(7.5)
    time.sleep(1)
    # Second reading
    for i in range(0,10,1):
        s2_array[i]=adc.read_adc(i, gain=GAIN)
        s2 = max(s1_array)

# Calculate hour angle
    # Apply sigmoid function
    a1 = 1/(math.pow(10, s1)+1)
    a2 = 1/(math.pow(10, s2)+1)
    # Trigonometric function operations
    b1 = 1 - 2*a1
    b2 = 1 - 2*a2
    c = (b1-b2)/(abs(b1)+abs(b2))
    # Calculate phi
    phi = -math.sqrt(3)*math.tan(2*phi-(pi/3)) #Need to check the sign of this

#Calculate longitude
