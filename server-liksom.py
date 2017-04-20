import time

import rfid.py
import berryclip.py 




card_1_id = b'K\x01\x01\x00\x04\x08\x04\xf0\xd0\xe6\x16'
card_2_id = b'K\x01\x01\x00\x04\x08\x04\xe2\x0fE\xf2'

def RFIDlookup (rfid_data):
## Scans a card then asks the server if the user is registered. Returns boolean value 0/1. 
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
	

def roomUserAccess (user_access):
	if user_access : 
		print("Access granted. ") 
		roomBehaviour()
	else :
		print("Access denied. ")
		setRedLED(1)



	