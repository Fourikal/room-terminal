import RPi.GPIO as GPIO



def init ():
        GPIO.setup(17, GPIO.OUT) 
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)



def setRedLED (value):
## Takes boolean values 0/1. 
	GPIO.output(17, value)
	
def setGreenLED (value):
## Takes boolean values 0/1. 
	GPIO.output(27, value)

def setYellowLED (value):
## Takes boolean values 0/1.
        GPIO.output(4, value)

def resetRoomLEDs ():
	setRedLED(0)
	setYellowLED(0)
	setGreenLED(0)




