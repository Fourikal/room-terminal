import time

import rfid
import berryclip
import tasks
import ir


t_sleepTime = 3
t_resetIR = t_sleepTime * 3
t_abandonnedRoom = t_resetIR

card_1_id = b'K\x01\x01\x00\x04\x08\x04\xf0\xd0\xe6\x16'
card_2_id = b'K\x01\x01\x00\x04\x08\x04\xe2\x0fE\xf2'

def RFIDlookup (rfid_data):
## Shall not be used in product. Is a simulation tool. 
## Scans a card then asks the server if the user is registered. Returns boolean value 0/1. 
	print("Request: User id lookup. ") ## Shall send to server. 

	## Simulate waiting for response from server. (show yellow LED while waiting.)
	berryclip.setYellowLED(1)	
	time.sleep(2) 	## Unrealistic wait time, but is easily visible. 
	#insert server communication here. 
	berryclip.setYellowLED(0)

	## A response has arrived. 
	reply = (rfid_data == card_2_id) #Lets assume user with card_2_id is a registered user, and that card_1_id is not a user. 

	if reply : ## If the response is 'accepted' then green led. Else (means 'rejected') then red led. 
		print("Found a user match. ")
		return 1
	else :
		print("User not found. ")
		return 0


def roomBehaviour ():
## Shall not be used in product. Is a simulation tool. 
	#send booking verification to server. (can booking and verification be combined? )
	print("Request: Verify room. ")

	## A response has arrived. 
	reply = 1 # what will the response look like? string, bool?

	if reply :
		print("Room is verified and ready for use. ")
		berryclip.setGreenLED(1)
		return

	print("Request: Book room. ")
	reply = 1

	if reply :
		print("Room is booked, verified and ready for use. ")
		berryclip.setGreenLED(1)
	else :
		print("Room is already booked by others. ")
		berryclip.setRedLED(1)
	

def roomUserAccess (user_access):
## Shall not be used in product. Is a simulation tool. 
	if user_access : 
		print("Access granted. ") 
		roomBehaviour()
	else :
		print("Access denied. ")
		berryclip.setRedLED(1)


def runIRtimer ():
## Decides when the IR shall declare the room 'empty'. 
	global t_abandonnedRoom
	ir_data = ir.read()

	if (ir_data == 1): ## Someone is present; restart timer. 
		t_abandonnedRoom = t_resetIR
		berryclip.resetRoomLEDs()
	else:
		t_abandonnedRoom -= t_sleepTime

	if (t_abandonnedRoom <= 0):
		## Nobody has been present for some time; tell server to cancel remaining reservation time. 
		#insert server communication here. 
		print("Room is empty!")
		tasks.setIRactivation(0)
		t_abandonnedRoom = t_resetIR

		## Be aware they may sit very still; maybe give a sound/LED warning?. 
		berryclip.setRedLED(1)
		time.sleep(t_sleepTime)
		berryclip.resetRoomLEDs()
		

