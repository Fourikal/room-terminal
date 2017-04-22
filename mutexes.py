import threading 



ir_timer_is_active = 0
ir_mutex = threading.Lock()



def setIRactivation (value):
## Takes boolean value 0/1. 
	ir_mutex.acquire()
	try :
		global ir_timer_is_active
		ir_timer_is_active = value
	finally :
		ir_mutex.release()











