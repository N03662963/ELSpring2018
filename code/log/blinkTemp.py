#!/usr/bin/python
import RPi.GPIO as GPIO
import os
import time
import sqlite3 as mydb
import sys

from flask import Flask, render_template
app = Flask(__name__)

#assign my pins
greenPin = 22
redPin = 27

#init GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)

#LED vars
#blink duration
blinkDur = 0.1

curTemp = 68

"""Log Curr Time, temp in celsius and fahrenheit to an sqlite3 database"""

def readTemp():
	global curTemp
	tempfile = open("/sys/bus/w1/devices/28-0000069616c4/w1_slave")
	tempfile_text = tempfile.read()
	currentTime = time.strftime("%x %X %Z")
	tempfile.close()
	tempC = float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF=tempC*9.0/5.0+32.0
	curTemp = tempF
	return [currentTime, tempC, tempF]

conn = mydb.connect('./temperature.db')
cur = conn.cursor()

def logTemp():
	with conn:
		try:
			[t,C,F] = readTemp()
			print "Current Temperature is: %s F" %F
			#sql = "insert into tempData values(?,?,?)"
			cur.execute('insert into templog values(?,?,?)', (t,C,F))
			print "Temperature logged"
		except:
			print "Error!!"

def print_table():
	table = conn.execute("select * from templog")
	os.system('clear')
	for row in table:
		print row

def blink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def every_min_read():
	oldTime = time.time()
	readTemp()
	print curTemp
	while True:
		if time.time() - oldTime > 59:
			logTemp()
			#readTemp()
			print_table()
			oldTime = time.time()
		if curTemp >= 68 and curTemp <= 78:
			GPIO.output(greenPin,True)
		else:
			GPIO.output(greenPin, False)
			blink(redPin)



try:
	#every_min_read()
	GPIO.cleanup()

except KeyboardInterrupt:
	os.system('clear')
	conn.close()
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()