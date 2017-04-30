import threading
import time

#import paho.mqtt.client as mqtt
#import json

import software.IRctrl as IRctrl
import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
import software.mutexes as mutexes
#import communication
import setupThreads as setupThreads
import software.LEDs as LEDs
import software.behaviour
import software.IRctrl as IRctrl



#class myThread(threading.Thread):
#    def __init__(self, threadID, name):
#        threading.Thread.__init__(self)
#        daemon = True  ## Enables all threads stop at keyboardInterrupt.
#        self.threadID = threadID
#        self.name = name
#
#    def run(self):
#        ## Will finish execution and exit thread, if code is not e.g. while(true).
#        print("Thread " + self.name + " is active.")
#
#        if (self.threadID == 1):
#            task_RFIDandLED()
#        elif (self.threadID == 2):
#            task_IR()
#
#        print("Thread " + self.name + " is terminated.")



def runTasks():
    ## Setup and start extra threads.
    ## thread_rfid = setupThreads.myThread(1, "RFID control")
    thread_ir = setupThreads.myThread(2, "IR control")

    ## thread_rfid.start()
    thread_ir.start()

    ## Start main execution thread.
    #print("RFID and LED is active.")
    task_RFIDandLED()



def task_simulateReadAndSendRFID():
	hardware.init()
	task_period = 3  ## Timing for the LEDs, mainly.
	
	while (True):
		card_data = rfid.read()
		user_access = simulateServer.RFIDlookup(card_data) #Simulate server communication.
		simulateServer.roomUserAccess(user_access)
		if (user_access):
			mutexes.setIRactivation(1)
			thread_ir = setupThreads.myThread(2, "IR control")
			thread_ir.start()
		time.sleep(task_period)
		LEDs.off()


def task_sendRFID ():
	hardware.init()
#	time.sleep(1)
#    client = mqtt.Client()
#    client.on_connect = on_connect
#    client.on_message = on_message
#    client.connect("iot.eclipse.org", 1883, 60)
	task_period = 2    ## Note that this is not truly a 'period', because of blocking RFID read. 

	while (True):
#		card_data = rfid.read()
#		print("Got data")
#		# SEND TO SERVER
#		communication.send_message(roomData.roomID, card_data, 'cardask')
#		card_data=None
		behaviour.readAndSendRFID()
		time.sleep(task_period)

def task_receiveUserAccess ():
	## Verified booking or Instant booking was received. 
	hardware.init()
	LEDs.blinkGreen

	mutexes.setIRactivation(1)
	thread_ir = setupThreads.myThread(2, "IR control")
	thread_ir.start()

def task_IR ():
	hardware.init()
	task_period = 3         ## Should be maximum 3 seconds. 

	while ( (mutexes.ir_timer_is_active) and (IRctrl.getTimerValue() > 0) ):
		IRctrl.runTimer()
		print("Remaining IR timer ticks: ", IRctrl.getTimerValue())
		time.sleep(task_period)
	
	mutexes.setIRactivation(0)

	print("Room is empty!")
	IRctrl.resetTimer()
	LEDs.blinkRed()



class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        daemon = True  ## Enables all threads stop at keyboardInterrupt.
        self.threadID = threadID
        self.name = name

    def run(self):
        ## Will finish execution and exit thread, if code is not e.g. while(true).
        print("Thread " + self.name + " is active.")

        if (self.threadID == 1):
            task_sendRFID()
        elif (self.threadID == 2):
            task_IR()

        print("Thread " + self.name + " is terminated.")


