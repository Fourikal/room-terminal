
import GPIOhardware.rfid as rfid
import software.LEDs as LEDs
import data.roomData as roomData
import software.communication as communication
import software.mutexes as mutexes



def readAndSendRFID ():
	card_data = rfid.read()
	print("Got RFID data. ")

	communication.send_message(roomData.roomID, card_data, 'cardask')
	card_data=None




