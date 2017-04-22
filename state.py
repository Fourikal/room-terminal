import time

import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
import GPIOhardware.ir as ir
import tasks













"""
COMMON STATES:
	logged out
		read rfid 
	read rfid 
		attempt login 
	attempt login 
		logged in 
		logged out 
	logged in (user access) 
		
		
	
ROOM STATES:
	logged in (user access) 
		ask server about user id reservations
	ask server about user id reservations
		reservation is now verified 	(user had reservations)
		room is now instant-booked 		(user had no reservations) 
		room is unavailable 			(user had no reservations) 
	reservation is now verified 	(user had reservations)
		display green LED 
	room is now instant-booked 		(user had no reservations) 
		display green LED 
	room is unavailable 			(user had no reservations) 
		display red LED 

	display green LED 
		active room (logged out?) 
	active room (logged out) 
		ir timeout 
		reservation time expired 

	ir timeout 
		display red LED 
	reservation time expired 
		display red LED 
	display red LED 
		logged out 
	

HALL STATES: 
	logged out
		read rfid 
		enter user id 
	enter user id 
		attempt login 
	logged in (user access)
		!!! timeout t1 
		ask server for user's room list (default) (restricted user access from false reservations?)
	ask server for user's room list 
		display room booking list 
	display room booking list 
		
		
	!!! timeout t1 
		logged out 


"""





