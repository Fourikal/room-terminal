import threading
import time
import paho.mqtt.client as mqtt
import json

import OldserverLiksom
import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
#import communication
import mutexes

t_LEDs = 2  ## LED timer; how long LED is active before turned off.

roomId=1
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

        # print("Thread " + self.name + " is terminated.")

def on_message(client, userdata, msg):
    data = json.dumps(str(msg.payload))[2:-1]
    print(data)
    if data[-1]['type']=='cardAsked':
        berryclip.setYellowLED(0)
        if data[-1]['response']=='confirmed' or data[-1]['response']=='booked':
            berryclip.setGreenLED(1)
        if data[-1]['response']=='denied':
            berryclip.setRedLED(1)

def on_connect(client, userdata, flags, rc):
    print(("connected with result code " + str(rc)))
    client.subscribe("/fk/rr/2")


def runTasks():
    ## Setup and start extra threads.
    # thread_rfid = myThread(1, "RFID control")
    # thread_ir = myThread(2, "IR control")
    # thread_rfid.start()
    # thread_ir.start()

    ## Start main execution thread.
    print("RFID and LED is active.")
    task_RFIDandLED()



def task_noServRFIDandLED():
    hardware.init()
    task_period = 3  ## Timing for the LEDs, mainly.
    while (True):
	card_data = rfid.read()
	OldserverLiksom.RFIDlookup(card_data)
	


def task_RFIDandLED():
    hardware.init()
    time.sleep(1)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("iot.eclipse.org", 1883, 60)
    
    task_period = 3  ## Timing for the LEDs, mainly.
    while (True):
        card_data = rfid.read()
        # SEND TO SERVER
        if card_data != None:
            print("got data")
            data = {'roomId': roomId, 'RFID': card_data.hex(), 'command': 'cardask'}
            client.publish('/fk/rr', json.dumps(data))
            card_data=None
            time.sleep(2)

'''	
def task_IR ():
	hardware.init()

	task_period = 3         ## Should be maximum 3 seconds. 
	#while (True):
	#	if (ir_timer_is_active):
	#		serverLiksom.runIRtimer()
	#	time.sleep(task_period)

	while (communication.getIRtimer() > 0):
		communication.runIRtimer()
		time.sleep(task_period)
	
	print("Room is empty!")

	mutexes.setIRactivation(0)
	communication.resetIRtimer()

	berryclip.setRedLED(1)
	time.sleep(t_LEDs)
	berryclip.resetRoomLEDs()
'''
