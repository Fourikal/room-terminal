import paho.mqtt.client as mqtt
import json
import time

import ..software.LEDs as LEDs



def on_connect(client, userdata, flags, rc):
	print(("Connected with result code " + str(rc)))
	client.subscribe("/fk/rr/2")

def on_message(client, userdata, msg):
	#data = json.dumps(str(msg.payload))[2:-1]

	## setYellowLED(1)
	#print("Yellow")
	#key = data['response']
	#if key == 'confirmed' or key == 'booked':
	#	# setGreenLED(1)
	#	print("Green")
	#elif key == 'denied':
	#	# setRedLED(1)
	#	print("Red")


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
		if melding['response'] == 'denied':
			LEDs.blinkRed()





roomId=1

client=mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
