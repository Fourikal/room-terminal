import threading 
import time

import hardware

import serverLiksom 
import rfid
import berryclip

ir_timer_is_active = 0
ir_mutex = threading.Lock()

def runTasks ():
	thread_rfid = myThread(1, "RFID control")
	thread_ir = myThread(2, "IR control")

	thread_rfid.start()
	thread_ir.start()



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
	hardware.init()
	task_period = 3
	while (True):
		card_data = rfid.read()
		user_access = serverLiksom.RFIDlookup(card_data)
		serverLiksom.roomUserAccess(user_access)
		if (user_access):
			setIRactivation(1)
		time.sleep(task_period)
		berryclip.resetRoomLEDs()
	
def IRtask ():
	hardware.init()
	task_period = 3         ## Should be at maximum 3 seconds. 
	while (True):
		if (ir_timer_is_active):
			serverLiksom.runIRtimer()
		time.sleep(task_period)

	
	
	
