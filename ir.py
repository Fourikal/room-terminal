import RPi.GPIO as GPIO
import time 

import berryclip.py 



t_resetIR = t_sleepTime * 3
t_abandonnedRoom = t_resetIR


def IRinit ():
	GPIO.setup(22, GPIO.IN)

def readIR ():
## Returns boolean value 0/1 dependent on movement within sight. 
	ir_data = GPIO.input(22)
	print(ir_data)
	return ir_data
	
def runIRtimer ():
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
		setIRactivation(0)
		t_abandonnedRoom = t_resetIR

		## Be aware they may sit very still; maybe give a sound/LED warning?. 
		setRedLED(1)
		time.sleep(t_sleepTime)
		resetRoomLEDs()
		

		


