import time
import GPIOhardware.berryclip as berryclip



t_LEDs = 2



def blinkRed ():
        berryclip.setRedLED(1)
        time.sleep(t_LEDs)
        berryclip.resetRoomLEDs()

def blinkYellow ():
	berryclip.setYellowLED(1)
	time.sleep(t_LEDs)
	berryclip.resetRoomLEDs()

def blinkGreen ():
        berryclip.setGreenLED(1)
        time.sleep(t_LEDs)
        berryclip.resetRoomLEDs()


