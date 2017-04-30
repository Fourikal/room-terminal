import RPi.GPIO as GPIO

import time

import GPIOhardware.hardware as hardware
#import GPIOhardware.rfid as rfid
#import communication.communication as communication
#import data.roomData as roomData
#import GPIOhardware.berryclip as berryclip
#from tasks import runTasks
import software.tasks as tasks
#import software.mutexes as mutexes
#import communication.outgoing as outgoing



## Main.
print("Main init. ")
hardware.init()

try:
#	while (True):
#		card_data = rfid.read()
#		print("Got data")
#		communication.send_message(roomData.roomID, card_data, 'cardask')
#		outgoing.send_message(roomData.roomID, card_data, 'cardask')
#		card_data=None
#		time.sleep(2)
#		mutexes.setIRactivation(1)
#		runTasks()
#		tasks.runTasks()
	tasks.runTasks()
finally: 
	print("Exiting. ")
	hardware.close()

