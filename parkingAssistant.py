import RPi.GPIO as GPIO
import time
import signal
import sys
import subprocess
import json

#Set GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 18
ECHO = 24

occupied = False

#close
def close(signal, frame):
	print("\nTurning off ultrasonic distance detection...\n")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, close)

#GPIO direction
def sensor_setup():
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)


#get distance of object 22
def distance():

	GPIO.output(TRIG, True)

	time.sleep(0.00001)

	GPIO.output(TRIG, False)

	startTime = time.time()
	stopTime = time.time()

	while 0 == GPIO.input(ECHO):
		startTime = time.time()

	while 1 == GPIO.input(ECHO):
		stopTime = time.time()

	TimeElapsed = stopTime - startTime


	distance = (TimeElapsed * 34300) / 2

	return distance


#Detect Object
def detection():
	if(distance() <= 7):
		print "detected"
		print distance()
	elif(distance() > 7):
		print "No detection"
		print distance()

	time.sleep(5)


#Convert to JSON
def convertJSON(occupied):
	dict_object = {
	"occupied": occupied
	}
	return json.dumps(dict_object)

#Initialize
def initialize():
	occupied = True if distance() < 7 else False
	convertJSON(occupied)
	print (occupied)



if __name__ == '__main__':

	sensor_setup()
	initialize()

	while True:
		detection()




