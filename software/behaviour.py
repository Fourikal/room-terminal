import GPIOhardware.rfid as rfid
import communication.communication as communication
import software.LEDs as LEDs
import software.mutexes as mutexes



def readAndSendRFID ():
	card_data = rfid.read()
	print("Got RFID data. ")
	communication.send_message(roomData.roomID, card_data, 'cardask')
	card_data=None

def receiveUserAccess ():
        ## Verified booking or Instant booking was received.
        LEDs.blinkGreen
        mutexes.setIRactivation(1)
        thread_ir = setupThreads.myThread(2, "IR control")
        thread_ir.start()

def receiveUserReject ():
        ## User cannot book the room.
        LEDs.blinkRed()





