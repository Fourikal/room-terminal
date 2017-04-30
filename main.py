import RPi.GPIO as GPIO

import time

import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
from tasks import runTasks
import communication.communication as communication
import data.roomData as roomData


## Main.
hardware.init()

while (True):
	card_data = rfid.read()
	print("Got data")
	berryclip.setYellowLED(1)
	communication.send_message(roomData.roomID, card_data, 'cardask')
	card_data=None
	time.sleep(2)


