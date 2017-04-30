import GPIOhardware.ir as ir



## Assume the IR sensor is read every third second. 
## The timeout then happens after 3 * t_resetIR seconds. 
## The total prototype timeout shall be 15 minutes (t_reset=300). 
# TODO: 3 is an unrealistic, low value. Used for debug. 
t_resetIR = 3	

t_abandonnedRoom = t_resetIR



def getTimerValue ():
	return t_abandonnedRoom

def runTimer ():
## Decides when the IR shall declare the room 'empty'. 
	ir_data = ir.read()

	if (ir_data == 1): ## Someone is present; restart timer. 
		resetTimer()
	else:
		decrementTimer()

def resetTimer ():
	global t_abandonnedRoom
	t_abandonnedRoom = t_resetIR
	
def decrementTimer ():
	global t_abandonnedRoom
	t_abandonnedRoom -= 1

def stopTimer ():
	global t_abandonnedRoom
	t_abandonnedRoom = 0

