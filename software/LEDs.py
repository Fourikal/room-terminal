import time

import GPIOhardware.berryclip as berryclip



t_LEDs = 2



def blinkRed ():
        berryclip.setRedLED(1)
        time.sleep(t_LEDs)
        berryclip.setRedLED(0)

def blinkYellow ():
	berryclip.setYellowLED(1)
	time.sleep(t_LEDs)
	berryclip.setYellowLED(0)

def blinkGreen ():
        berryclip.setGreenLED(1)
        time.sleep(t_LEDs)
        berryclip.setGreenLED(0)

def setYellow (value):
	berryclip.setYellowLED(value)

def off ():
        berryclip.resetRoomLEDs()


