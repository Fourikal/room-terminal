#import RPi.GPIO as GPIO

from tasks import runTasks




## Main. 
try: 
	runTasks()

	## todo: 
	# solve polling/interrupt. careful around the blocking rfid read. threads?
	# insert server communication in this code. not my task to create; will wait for usable functions. 		
	# rfid shall also handle instant-booking. 




	#GPIO.cleanup()
        
except KeyboardInterrupt: 
        #GPIO.cleanup()
        print("bye")
