import threading

import tasks



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
            tasks.task_RFIDandLED()
        elif (self.threadID == 2):
            tasks.task_IR()

        print("Thread " + self.name + " is terminated.")


