#import RPi.GPIO as GPIO

#import GPIOhardware.hardware as hardware
from tasks import runTasks



## Main. 
try: 
	runTasks()



	## todo: 
	# insert server communication in this code. not my task to create; will wait for usable functions. 		
	# rfid shall also handle instant-booking. 
	# what happens when one scans card again after logged in?
	# create a clearer state-machine view. (same behaviour)


	
	#GPIO.cleanup()
	#hardware.close()
	
except KeyboardInterrupt: 
        #GPIO.cleanup()
	#hardware,close()
	print("bye")


