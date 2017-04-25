from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

pn532 = Pn532_i2c()
pn532.SAMconfigure()



def read ():
## This function is blocking. 
	card_data = pn532.read_mifare().get_data()
	#print(card_data)
	return card_data	

	
	
	
