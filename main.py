import RPi.GPIO as GPIO

import time

import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import communication.communication as communication
import data.roomData as roomData
import GPIOhardware.berryclip as berryclip
from tasks import runTasks
import software.mutexes as mutexes

## Main.
hardware.init()

try:
#	while (True):
#		card_data = rfid.read()
#		print("Got data")
#		communication.send_message(roomData.roomID, card_data, 'cardask')
#		card_data=None
#		time.sleep(2)
#		mutexes.setIRactivation(1)
#		runTasks()
	runTasks()

finally: 
	print("Exiting. ")
	hardware.close()


