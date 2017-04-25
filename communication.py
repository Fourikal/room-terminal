import paho.mqtt.client as mqtt
import json
import time

def on_connect(client, userdata, flags, rc):
    print(("connected with result code " + str(rc)))
    client.subscribe("/fk/rr/2")

def on_message(client, userdata, msg):
    data = json.dumps(str(msg.payload))[2:-1]

    # setYellowLED(1)
    print("Yellow")
    key = data['response']
    if key == 'confirmed' or key == 'booked':
        # setGreenLED(1)
        print("Green")
    elif key == 'denied':
        # setRedLED(1)
        print("Red")

roomId=1

client=mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
