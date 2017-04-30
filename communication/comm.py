import paho.mqtt.client as mqtt
import json
import time

import software.LEDs as LEDs
import data.roomData as roomData
import software.mutexes as mutexes
#import software.behaviour as behaviour 
import tasks



client=mqtt.Client()
client.loop_start()
client.connect(roomData.CHANNEL_CONNECT, 1883, 60)



def on_connect (client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(roomData.CHANNEL_SUB)

def on_message (client, userdata, msg):
	data = json.loads(msg.payload)
	melding = data[0]

#	behaviour.receiveMessage(melding)

	if melding['type'] == 'error':
		print("Error")
		time.sleep(1)
		LEDs.off()
	elif melding['type'] == 'cardAsked':
		print("Cardask")
		LEDs.off()
		if melding['response'] == 'confirmed' or data[-1]['response'] == 'booked':
			LEDs.blinkGreen()
			receiveUserAccept()
		if melding['response'] == 'denied':
			LEDs.blinkRed()
			receiveUserReject()


def send_message (roomID, card_data, commandType):
	print("comm.send")
	LEDs.setYellow(1)
	data = {'roomId': roomID, 'RFID': card_data.hex(), 'command': commandType}
	client.publish(roomData.CHANNEL_PUB, json.dumps(data))



client.on_connect = on_connect
client.on_message = on_message


def receiveUserAccept ():
        ## Verified booking or Instant booking was received.
        LEDs.off()
        LEDs.blinkGreen
        mutexes.setIRactivation(1)
        thread_ir = tasks.myThread(2, "IR control")
        thread_ir.start()

def receiveUserReject ():
        ## User cannot book the room.
        LEDs.off()
        LEDs.blinkRed()




