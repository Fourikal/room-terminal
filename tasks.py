import threading 
import time

import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
import serverLiksom



ir_timer_is_active = 0
ir_mutex = threading.Lock()



class myThread (threading.Thread):
	def __init__ (self, threadID, name):
		threading.Thread.__init__(self)
		daemon = True 		## Enables all threads stop at keyboardInterrupt. 
		self.threadID = threadID 
		self.name = name

	def run (self): 
	## Will finish execution and exit thread, if code is not e.g. while(true). 
		print("Thread " +  self.name + " is active.")
		
		#if (self.threadID == 1):
		#	task_RFIDandLED()
		#elif (self.threadID == 2):
		#	task_IR()

		try :
			if (self.threadID == 1):
				task_RFIDandLED()
			elif (self.threadID == 2):
				task_IR()
		except :
			print("Thread-zone!")
		finally :
			print("zone thread 2")
		
		print("Thread " + self.name + " is terminated.")



def runTasks ():
	## Setup and start extra threads.
	#thread_rfid = myThread(1, "RFID control")
	thread_ir = myThread(2, "IR control")

	#thread_rfid.start()
	thread_ir.start()

	## Start main execution thread. 
	print("RFID and LED is active.")
	task_RFIDandLED()
	while threading.active_count() > 0:
		time.sleep(0.1)


def setIRactivation (value):
## Takes boolean value 0/1. 
	ir_mutex.acquire()
	try :
		global ir_timer_is_active
		ir_timer_is_active = value
	finally :
		ir_mutex.release()



def task_RFIDandLED ():
	hardware.init()

	task_period = 3         ## Timing for the LEDs, mainly. 
	while (True):
		card_data = rfid.read()
		user_access = serverLiksom.RFIDlookup(card_data)
		serverLiksom.roomUserAccess(user_access)
		if (user_access):
			setIRactivation(1)
		time.sleep(task_period)
		berryclip.resetRoomLEDs()
	
def task_IR ():
	hardware.init()
	task_period = 3         ## Should be maximum 3 seconds. 
	while (True):
		if (ir_timer_is_active):
			serverLiksom.runIRtimer()
		time.sleep(task_period)

	
	
	
