from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import time
 
pn532 = Pn532_i2c()
pn532.SAMconfigure()
 

while True:
	card_data = pn532.read_mifare().get_data()
	print(card_data)
	time.sleep(5)