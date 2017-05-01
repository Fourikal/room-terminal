import time
#import RPi.GPIO as GPIO

import GPIOhardware.hardware as hardware
#import GPIOhardware.rfid as rfid
#import software.communication as communication
#import data.roomData as roomData
#import software.mutexes as mutexes
import software.tasks as tasks



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

