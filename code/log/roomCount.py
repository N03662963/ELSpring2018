import time
import RPi.GPIO as GPIO
import os
import sqlite3 as mydb
import sys

#Assign gpio pins. 13 is for entering. 26 is for leaving.
hallPin = 17
roomPin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(camPin1, GPIO.IN)
GPIO.setup(camPin2, GPIO.IN)

#FOR EVERYTHING BELOW I REFER TO THE FIRST AND SECOND SENSORS. THAT DOESN'T REFER TO THE POSITION OF THE SENSORS,
#IT REFERS TO THE ORDER THAT THEY ARE TRIGGERED IN.

#Here is the thing.  This is not going to work so well because both sensors will be triggered regardless of
#If a person is entering or leaving.  It's the order that they are triggered that determines if someone is entering or leaving.
#I would set this up differently. The first thing I would do would be to create a function that is triggereg whenever either sensor goes off,
#and then listens for the second sensor to be triggered. You are also going to need to add a check in there in case the second sensor isn't triggered.
#Something like:

def bothTriggers(trigger2, wait=5):
	timeStamp = False
	#This is the sanity check.  If the second sensor isn't triggered, it resets.
	#The sanity check only happens while the second sensor is in a low state (not triggered)
	timeCheck = time.time()
	while not GPIO.input(trigger2):
		if time.time() - timeCheck > wait:
            break
        continue
    #If the second sensor is triggered, it bypasses the previous if statement and creates the timestamp
    #The it waits for 5 seconds to let the sensors reset. Adjust the sleep timer to the time it takes 
    #for both of your sensors to reset.
    if time.time() - timeCheck <= wait:
        timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
        time.sleep(4)
        continue

#Now you need to rewrite all of this.  You need 2 if statements, one for each sensor.
#When the first sensor is triggered, it should pass the variable for the second sensor's pin.

#let the camera have time to set up
time.sleep(10)
#Set the initial count to zero
roomCount = 0

#Now you need to write all of this.  You need to fill in the 2 if statements, one for each sensor.
#When the first sensor is triggered, it passes the variable for the second sensor's pin to the function that
#listens for both of the triggers.

try:
	while True:
		#Connect to the database udsr variables as globals
		#Also make sure you actually created the database and table in your log folder
		con = mydb.connect('log/room.db')
		cur = con.cursor()
		#Reset timeStamp to false to prevent writing data until both sensors are triggered again
		timeStamp = False
        
        if GPIO.input(hallPin):
			timeStamp = bothTriggers(roomPin)
			if timeStamp:
#Write a bit here that sets a variable to show that a person entered the room. Increase the roomCount +1
		if GPIO.input(roomPin):
			timeStamp = bothTriggers(hallPin)
			if timeStamp:
#Write a bit here that set a variable to show that a person left the room. Decrease the roomCount -1

#Since the timeStamp is only set when the direction is determined and both sensors are triggered we use that as the condition to write our data:
		if timeStamp:
#Write a bit here to log the timeSamp, if the person was entering or exiting, and the room count after they entered or exited.

except mydb.Error, e:
	print "Error %s:" %e.args[0]
	sys.exit(1)

except KeyboardInterrupt:
        GPIO.cleanup()
        con.close()
        print('Exited Cleanly')
roomCount.py
Zoomed into item.