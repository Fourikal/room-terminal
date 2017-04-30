import paho.mqtt.client as mqtt
import json
import time

import data.roomData as roomData

from . import LEDs as LEDs
from . import mutexes as mutexes
from . import tasks as tasks



#client=mqtt.Client()
#client.connect(roomData.CHANNEL_CONNECT, 1883, 60)
#client.loop_start()



def on_connect (client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(roomData.CHANNEL_SUB)

def on_message (client, userdata, msg):
	print("Received a message. ")
	data = json.loads(msg.payload)
	melding = data[0]

	if melding['type'] == 'error':
		print("Error")
		time.sleep(1)
		LEDs.off()
	elif melding['type'] == 'cardAsked':
		print("Cardask")
		LEDs.off()
		if melding['response'] == 'confirmed' or data[-1]['response'] == 'booked':
			LEDs.blinkGreen()
#			receiveUserAccept()
		if melding['response'] == 'denied':
			LEDs.blinkRed()

def send_message (roomID, card_data, commandType):
	print("comm.send")
	LEDs.setYellow(1)
	data = {'roomId': roomID, 'RFID': card_data.hex(), 'command': commandType}
	client.publish(roomData.CHANNEL_PUB, json.dumps(data))

client=mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect(roomData.CHANNEL_CONNECT, 1883, 60)
client.loop_start()



def receiveUserAccept ():
        ## Verified booking or Instant booking was received.
        mutexes.setIRactivation(1)
        thread_ir = tasks.myThread(2, "IR control")
        thread_ir.start()





