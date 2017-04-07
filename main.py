from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
import RPi.GPIO as GPIO
 
pn532 = Pn532_i2c()
pn532.SAMconfigure()
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN)

while True:
	card_data = pn532.read_mifare().get_data()
	print(card_data)
	#print(GPIO.input(22))
	time.sleep(5)