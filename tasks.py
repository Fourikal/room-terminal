import threading 
import time

import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
import serverLiksom
import mutexes



t_LEDs = 2	## LED timer; how long LED is active before turned off. 



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
			task_RFIDandLED()
		elif (self.threadID == 2):
			task_IR()

#		try :
#			if (self.threadID == 1):
#				task_RFIDandLED()
#			elif (self.threadID == 2):
#				task_IR()
#		except :
#			print("Thread exception!")
#		finally :
#			print("Thread " + self.name + " succesfully terminated")
		
		#print("Thread " + self.name + " is terminated.")



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



def task_RFIDandLED ():
	hardware.init()

	task_period = 3         ## Timing for the LEDs, mainly. 
	while (True):
		card_data = rfid.read()
		user_access = serverLiksom.RFIDlookup(card_data)
		serverLiksom.roomUserAccess(user_access)
		if (user_access):
			mutexes.setIRactivation(1)
			thread_ir = myThread(2, "IR control")
			thread_ir.start()
		time.sleep(task_period)
		berryclip.resetRoomLEDs()
	
def task_IR ():
	hardware.init()

	task_period = 3         ## Should be maximum 3 seconds. 
	#while (True):
	#	if (ir_timer_is_active):
	#		serverLiksom.runIRtimer()
	#	time.sleep(task_period)

	while ( serverLiksom.getIRtimer() > 0 ):	
		serverLiksom.runIRtimer()
		time.sleep(task_period)
	
	print("Room is empty!")

	mutexes.setIRactivation(0)
	serverLiksom.resetIRtimer()

	berryclip.setRedLED(1)
	time.sleep(t_LEDs)
	berryclip.resetRoomLEDs()
	
	
	
