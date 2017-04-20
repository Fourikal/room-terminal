import RPi.GPIO as GPIO

import mythreads.py 



def GPIOinit ():
	GPIO.setmode(GPIO.BCM)
	IRinit()
	LEDinit()
 
GPIOinit()

## Main. 
try: 
	## step 6: threads for multiple simultaneous running program parts. 
	thread_rfid = myThread(1, "RFID control")
	thread_ir = myThread(2, "IR control")

	thread_rfid.start()
	thread_ir.start()

	## todo: 
	# solve polling/interrupt. careful around the blocking rfid read. threads?
	# insert server communication in this code. not my task to create; will wait for usable functions. 		
	# rfid shall also handle instant-booking. 


except KeyboardInterrupt: 
	GPIO.cleanup()
