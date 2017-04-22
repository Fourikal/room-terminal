import RPi.GPIO as GPIO



import GPIOhardware.ir as ir 
import GPIOhardware.berryclip as berryclip



def init ():
    GPIO.setmode(GPIO.BCM)
    ir.init()
    berryclip.init()

def close ():
    GPIO.cleanup()


