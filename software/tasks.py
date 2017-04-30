import threading
import time

import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import data.roomData as roomData

from . import IRctrl as IRctrl
from . import mutexes as mutexes
from . import LEDs as LEDs
from . import communication as communication



def runTasks():
    ## Setup and start extra threads.
    #thread_rfid = myThread(1, "RFID control")
    #thread_ir = myThread(2, "IR control")

    #mutexes.setIRactivation(1)
    #thread_rfid.start()
    #thread_ir.start()

    ## Start main execution thread.
    #print("RFID and LED is active.")
    task_sendRFID()

def task_sendRFID ():
#	hardware.init()
	time.sleep(1)
	t_taskPeriod = 2    ## Note that this is not truly a 'period', because of the blocking RFID read. 

	while (True):
		card_data = rfid.read()
		print("Got RFID data. ")

		communication.send_message(roomData.roomID, card_data, 'cardask')
		card_data=None

		time.sleep(t_taskPeriod)

def task_IR ():
	hardware.init()
	t_taskPeriod = 3         ## Should be maximum 3 seconds. 

	while ( (mutexes.ir_timer_is_active) and (IRctrl.getTimerValue() > 0) ):
		IRctrl.runTimer()
		print("Remaining IR timer ticks: ", IRctrl.getTimerValue())
		time.sleep(t_taskPeriod)
	
	mutexes.setIRactivation(0)

	print("Room is empty!")
	IRctrl.resetTimer()
	LEDs.blinkRed()

def task_simulateReadAndSendRFID():
        hardware.init()
        t_taskPeriod = 3  ## Timing for the LEDs, mainly.

        while (True):
                card_data = rfid.read()
                user_access = simulateServer.RFIDlookup(card_data) #Simulate server communication.
                simulateServer.roomUserAccess(user_access)
                if (user_access):
                        mutexes.setIRactivation(1)
                        thread_ir = setupThreads.myThread(2, "IR control")
                        thread_ir.start()
                time.sleep(t_taskPeriod)
                LEDs.off()



class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        daemon = True  ## Enables all threads stop at keyboardInterrupt.
        self.threadID = threadID
        self.name = name

    def run(self):
        ## Will finish execution and exit thread, if code is not e.g. while(true).
        print("Thread " + self.name + " is active.")

        if (self.threadID == 1):
            task_sendRFID()
        elif (self.threadID == 2):
            task_IR()

        print("Thread " + self.name + " is terminated.")


