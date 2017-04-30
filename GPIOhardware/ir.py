import RPi.GPIO as GPIO



def init ():
	GPIO.setup(22, GPIO.IN)



def read ():
## Returns boolean value 0/1 dependent on movement within sight. 
        ir_data = GPIO.input(22)
        #print(ir_data)
        return ir_data

		


