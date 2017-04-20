import threading 
from threading import Lock
import time

#import rfid.py 
#import berryclip.py 
import server-liksom.py 
import ir.py 



t_sleepTime = 3		## IR sensor has approximately 3 s signal when discovering movement. 
 
ir_timer_is_active = 0
ir_mutex = Lock()


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
			RFIDandLEDtask()
		elif (self.threadID == 2):
			IRtask()

		print("Thread " + self.name + " is terminated.")



def setIRactivation (value):
## Boolean value 0/1. 
	ir_mutex.acquire()
	try :
		global ir_timer_is_active
		ir_timer_is_active = value
	finally :
		ir_mutex.release()


def RFIDandLEDtask ():
	while (True):
		card_data = readRFID()
		user_access = RFIDlookup(card_data)
		roomUserAccess(user_access)
		if (user_access):
			#global ir_timer_is_active
			#ir_timer_is_active = 1
			setIRactivation(1)
		time.sleep(t_sleepTime)
		resetRoomLEDs()
	
def IRtask ():
	while (True):
		if (ir_timer_is_active):
			runIRtimer()
		time.sleep(t_sleepTime)

	
	
	