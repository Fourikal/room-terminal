import RPi.GPIO as GPIO


def init ():
	GPIO.setmode(GPIO.BCM)

def setup (pin, type):
	if (type == 0):
		GPIO.setup(pin, GPIO.IN) 
	elif (type == 1):
		GPIO.setup(pin, GPIO.OUT) 
	else :
		print("gpio.init(): Wrong type input. ")

def output (pin, value):
	GPIO.output(pin, value)
	
def input (pin):
	return GPIO.input(pin)




