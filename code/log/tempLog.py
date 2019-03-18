#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import sqlite3
import time
import os

def create_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def create_temperature(conn, temp):
    sql = ''' INSERT INTO templog2(Date, Temperature)
                VALUES (?,?)'''
    cur = conn.cursor()
    com = conn.commit()
    cur.execute(sql, temp)
    return cur.lastrowid

def print_database(conn):
    sql = (''' SELECT * FROM templog2''')
    cur = conn.cursor()
    cur.execute(sql)
    for row in cur:
        print(row)

#Assign GPIO pins
redPin = 27
greenPin = 22
tempPin = 17
#buttonPin = 26

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11
#LED Variables-----------------------------------------------------------------------------------------
#Duration of each Blink
blinkDur = .1
#Number of times to Blink the LED
blinkTime = 7
timePassed = 0
#-----------------------------------------------------------------------------------------------------

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
#GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}*F'.format(temperature)
	else:
		print('Error Reading Sensor')
	
	return tempFahr

#def readH():
#	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
#	if humidity is not None and temperature is not None:
#		humid = '{1:0.1f}%'.format(temperature, humidity)
#

#Use the blinkonce function in a loopity-loop when the button is pressed
try:
    with open("../log/templog.csv", "a") as log:

	    while True:
               # input_state = GPIO.input(buttonPin)
               # if input_state == False:			
                    for i in range (blinkTime):
                        oneBlink(redPin)
                    time.sleep(60)
                    timePassed = timePassed + 60
                    timePassed = timePassed // 60
                    # clear the console
                   # os.system('clear')
                    data = readF(tempPin)
                    log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(data)))
                    temp_data = ("{0}".format(time.strftime("%Y-%m-%d %H:%M:%S")),"{0}".format(str(data)))
                    conn = create_db('./temperature.db')
                    with conn:
                        id = create_temperature(conn, temp_data)
                        
                    
			
except KeyboardInterrupt:
    #os.system('clear')
    print('Thanks for Blinking and Thinking!')
    GPIO.cleanup()
    conn.close()
