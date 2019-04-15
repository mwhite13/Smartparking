#Libraries
import RPi.GPIO as GPIO
import time
import signal
import sys
import subprocess
import json
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

occupied = False
 
#set GPIO direction (IN / OUT)

def setup():
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def init_check():
    occupied = True if distance() >= 7 else False
    print "Occupied" 

#set distance
def distance():
    #set trigger to LOW
    GPIO.output(GPIO_TRIGGER, False)
    print "Waiting......."
    time.sleep(1)
    # set Trigger to HIGH
    print "Calculating ......"
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed  *17150)
    distance = round(distance, 2)
 
    return distance
 
if __name__ == '__main__':

    setup()
    init_check()
    try:
        while True:
          if(occupied and (distance()>= 7))or(not occupied and (distance() <7)):
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
