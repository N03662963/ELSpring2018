#import libs
import time
import RPi.GPIO as GPIO
import os
import sqlite3
import sys


#Assign gpio pins. 13 is for entering. 26 is for leaving.
hallPin = 13
roomPin = 26 

GPIO.setmode(GPIO.BCM)
GPIO.setup(hallPin, GPIO.IN)
GPIO.setup(roomPin, GPIO.IN)

# This function is passed the pin that has been triggered.
# We will wait 3 seconds. If the next pin is triggered, we will increment or decrement the roomcount.
# Otherwise, we will return to our main loop (since both triggers have not been activated).

#sqlite stuff
mydb = sqlite3.connect("./room.db")
cursor = mydb.cursor()
#mydb.commit()

#initialize variables and wait for sensors to start up 
time.sleep(10)
roomcount = 0

def bothTriggers(trigger2, wait=5):    
    timeStamp = False
	#This is the sanity check.  If the second sensor isn't triggered, it resets.
	#The sanity check only happens while the second sensor is in a low state (not triggered)
    timeCheck = time.time()
    print("Received Trigger: %d", trigger2)
    while not GPIO.input(trigger2):
        if time.time() - timeCheck > wait:
            break 
        else: continue
    #If the second sensor is triggered, it bypasses the previous if statement and creates the timestamp
    #The it waits for 5 seconds to let the sensors reset. Adjust the sleep timer to the time it takes 
    #for both of your sensors to reset.
    time.sleep(4)
    return timeStamp

#This is our main loop. If we receive a trigger, we send the opposing sensor's pin number to our 
#Triggers function. We listen for the other trigger. If it goes off in under 5 seconds, we have a positive
#otherwise, we continue polling after waiting for 4 seconds (to prevent a false-positive).
print("Listening for changes!")
try:
    while True:
        #Connect to the database udsr variables as globals
	#Also make sure you actually created the database and table in your log folder
	#cur = con.cursor()
	
        #Reset timeStamp to false to prevent writing data until both sensors are triggered again
	timeStamp = False
        place = "Empty"

        if GPIO.input(hallPin):
	    timeStamp = bothTriggers(roomPin)
            if timeStamp:
                place = "Entry"
                roomcount+=1
                timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
		print(timeStamp)
                print("Someone entered the room. The current room count:%d", roomcount)
                #push time and roomcount to the database (use function)
                #push_toDB(timestamp, roomcount)
                cursor.execute('''INSERT INTO rooms VALUES(?,?,?)''', (timeStamp, place, roomCount))
		mydb.commit()
		all_rows = cursor.execute('''SELECT * FROM rooms''')
		os.system('clear')
		for row in all_rows:
			print('{0} : {1} : {2}'.format(str(row[0]), row[1], str(row[2])))
                            
        if GPIO.input(roomPin):
	    timeStamp = bothTriggers(hallPin)
	    if timeStamp:
                place = "Exit"
                roomcount-=1
                timeStamp = time.strftime("%Y-%m-%d %H:%M:%S")
		print(timeStamp)
                print("Someone exited the room. The current room count: %d", roomcount)
                #push time and roomcount to the database (use function)
                #push_toDB(timestamp, roomcount)
                cursor.execute('''INSERT INTO rooms VALUES(?,?,?)''', (timeStamp, place, roomCount))
		mydb.commit()
		all_rows = cursor.execute('''SELECT * FROM rooms''')
		os.system('clear')
		for row in all_rows:
			print('{0} : {1} : {2}'.format(str(row[0]), row[1], str(row[2])))
		
        

except mydb.Error, e:
	print "Error %s:" %e.args[0]
	sys.exit(1)

except KeyboardInterrupt:
        GPIO.cleanup()
        mydb.close()
        print('Exited Cleanly')


