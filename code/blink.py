#Import libraries
import RPi.GPIO as GPIO
import time
import os

#initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#this function will make the light blink once
def blinkOnce(pin):
	GPIO.output(pin,True)
	time.sleep(.1)
	GPIO.output(pin, False)
	time.sleep(.1)

#call the blinkonce function above in a loop
try:
    while True:
        input_state = GPIO.input(26)
        if input_state == False:
            for i in range(10):
                blinkOnce(17)
            time.sleep(.2)

#cleanup the gpio when done
except KeyboardInterrupt:
    os.system('clear')
    print('Thanks for Blinking and Thinking!')
    GPIO.cleanup()
