from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import RPi.GPIO as GPIO
import threading 
 
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
## Returns boolean value 0/1 dependent on movement within sight. 
	ir_data = GPIO.input(22)
	print(ir_data)
	return ir_data


t_resetIR = t_sleepTime * 3
t_abandonnedRoom = t_resetIR

def IRtimer ():
## Decides when the IR shall declare the room 'empty'. 
	global t_abandonnedRoom
	ir_data = readIR()

	if (ir_data == 1): ## Someone is present; restart timer. 
		t_abandonnedRoom = t_resetIR
		resetRoomLEDs()
	else:
		t_abandonnedRoom -= t_sleepTime

	if (t_abandonnedRoom <= 0):
		## Nobody has been present for some time; tell server to cancel remaining reservation time. 
		#insert server communication here. 
		print("Room is empty!")
		
		## Be aware they may sit very still; maybe give a sound/LED warning?. 
		setRedLED(1)


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

def RFIDlookup (rfid_data):
## Scans a card then asks the server if the user is registered. Returns boolean value 0/1. 
	#rfid_data = readRFID()
	
	print("Request: User id lookup. ") ## Shall send to server. 

	## Simulate waiting for response from server. (show yellow LED while waiting.)
	setYellowLED(1)	
	time.sleep(2) 	## Unrealistic wait time, but is easily visible. 
	#insert server communication here. 
	setYellowLED(0)

	## A response has arrived. 
	reply = (rfid_data == card_2_id) #Lets assume user with card_2_id is a registered user, and that card_1_id is not a user. 

	if reply : ## If the response is 'accepted' then green led. Else (means 'rejected') then red led. 
		print("Found a user match. ")
		return 1
	else :
		print("User not found. ")
		return 0


def roomBehaviour ():
	#send booking verification to server. (can booking and verification be combined? )
	print("Request: Verify room. ")

	## A response has arrived. 
	reply = 1 # what will the response look like? string, bool?

	if reply :
		print("Room is verified and ready for use. ")
		setGreenLED(1)
		return

	print("Request: Book room. ")
	reply = 1

	if reply :
		print("Room is booked, verified and ready for use. ")
		setGreenLED(1)
	else :
		print("Room is already booked by others. ")
		setRedLED(1)
	

def room_userAccess (user_access):
	if user_access : 
		print("Access granted. ") 
		roomBehaviour()
	else :
		print("Access denied. ")
		setRedLED(1)



class myThread (threading.Thread):
	def __init__ (self, threadID, name):
		threading.Thread.__init__(self)
		daemon = True 		## Enables all threads stop at keyboardInterrupt. 
		self.threadID = threadID 
		self.name = name

	def run (self): 
	## Will finish execution and exit thread, if code is not e.g. while(true). 
		print("Thread " +  self.name + " is active.")

		if (self.threadID == 1):
			RFIDandLEDtest()
		elif (self.threadID == 2):
			IRtest()

		print("Thread " + self.name + " is terminated.")


ir_timer_is_active = 0

def RFIDandLEDtest ():
	while (True):
		card_data = readRFID()
		user_access = RFIDlookup(card_data)
		room_userAccess(user_access)
		if (user_access):
			global ir_timer_is_active
			ir_timer_is_active = 1
		time.sleep(t_sleepTime)
		resetRoomLEDs()
	
def IRtest ():
	while (True):
		if (ir_timer_is_active):
			IRtimer()
		time.sleep(t_sleepTime)



## Main. 
try: 
	## step 5: combine rfid and leds. 
	#while True:
		#card_data = readRFID()
		#user_access = RFIDlookup(card_data)
		#room_userAccess(user_access)

	## step 6: threads for multiple simultaneous running program parts. 
	thread_rfid = myThread(1, "RFID control")
	thread_ir = myThread(2, "IR control")

	thread_rfid.start()
	thread_ir.start()

	## todo: 
	# solve polling/interrupt. careful around the blocking rfid read. threads?
	# insert server communication in this code. not my task to create; will wait for usable functions. 		
	# create libraries/include files to tidy code, if time allows. 
	# rfid shall also handle instant-booking. 

	#time.sleep(t_sleepTime)
	#resetRoomLEDs()


except KeyboardInterrupt: 
	GPIO.cleanup()
