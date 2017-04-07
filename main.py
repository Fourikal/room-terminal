
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import RPi.GPIO as GPIO
 
pn532 = Pn532_i2c()
pn532.SAMconfigure()

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)

t_sleepTime = 3		## IR sensor has approximately 3 s signal when discovering movement. 




def readRFID ():
	## This function is blocking. 
	card_data = pn532.read_mifare().get_data()
	print(card_data)
	return card_data	

def readIR ():
	ir_data = GPIO.input(22)
	print(ir_data)
	return ir_data


t_abandonnedRoom = 0

def IRlogic ():
	global t_abandonnedRoom
	ir_data = readIR()

	if (ir_data == 1):
		## Someone is present; restart timer. 
		t_abandonnedRoom = 0
	else:
		t_abandonnedRoom += t_sleepTime

	if (t_abandonnedRoom >= (t_sleepTime * 3)):
		## Nobody has been present for some time; tell server to cancel remaining reservation time. 
		print("Room is empty!")
		## Be aware they may sit very still; maybe give a sound/LED warning?. 
		setYellowLED(1)


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

def roomLEDs ():
## Flash the LEDS on and off to indicate ok. 
	print("Running roomLEDs(). ")
	#GPIO.output(17, (GPIO.input(17) ^ 1))
	setRedLED(GPIO.input(17) ^ 1)
	setGreenLED(GPIO.input(27) ^ 1)
	setYellowLED(GPIO.input(4) ^ 1)

def resetRoomLEDs ():
	setRedLED(0)
	setYellowLED(0)
	setGreenLED(0)


card_1_id = b'K\x01\x01\x00\x04\x08\x04\xf0\xd0\xe6\x16'
card_2_id = b'K\x01\x01\x00\x04\x08\x04\xe2\x0fE\xf2'

def RFIDlogic ():
	rfid_data = readRFID()
	#take action for poorly read card id? or just send to server anyway? 
	print("Request: User id lookup. ")

	#(show yellow LED while waiting.)
	setYellowLED(1)	
	time.sleep(2)
	setYellowLED(0)
	
	if rfid_data == card_2_id : #b'K\x01\x01\x00\x04\x08\x04\xf0\xd0\xe6\x16' :
		#if response is 'accepted' then green led. 
		print("User match found. ")
		setGreenLED(1)
	else :
		#else (means rejected) then red led. 
		print("No user found. ")
		setRedLED(1)


## Main. 
try: 
	while True:
		## step 1: find out how rfid works. 
		#readRFID()
		#time.sleep(5)
	
		## step 2: find out how ir sensor works. 
		#out = readIR()
		#print(out)
		#time.sleep(5)
		
		## step 3: make ir behaviour prototype. 
		#IRlogic()
		#time.sleep(3)
	
		## step 4: find out how berryclip leds works. 
		#roomLEDs()

		## step 5: combine rfid and leds. 
		RFIDlogic()
		

		time.sleep(t_sleepTime)
		resetRoomLEDs()


except KeyboardInterrupt: 
	GPIO.cleanup()



