import RPi.GPIO as GPIO

import ir
import berryclip

def init ():
    GPIO.setmode(GPIO.BCM)
    ir.init()
    berryclip.init()

def close ():
    GPIO.cleanup()
