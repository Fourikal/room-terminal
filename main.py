import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
import GPIOhardware.ir as ir
import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
from tasks import runTasks


roomId=1
## Main.

hardware.init()
berryclip.setYellowLED(0)
berryclip.setGreenLED(0)
berryclip.setRedLED(0)
def on_message(client, userdata, msg):
        data = json.loads(msg.payload)
        melding=data[0]
        if melding['type']=='error':
                print("error")
                time.sleep(1)
                berryclip.setYellowLED(0)
        elif melding['type']=='cardAsked':
                print("cardask")
                berryclip.setYellowLED(0)
                if melding['response']=='confirmed' or data[-1]['response']=='booked':
                    berryclip.setGreenLED(1)
                    time.sleep(2)
                    berryclip.setGreenLED(0)
                if melding['response']=='denied':
                    berryclip.setRedLED(1)
                    time.sleep(2)
                    berryclip.setRedLED(0)

def on_connect(client, userdata, flags, rc):
    print(("connected with result code " + str(rc)))
    client.subscribe("/fk/rr/2")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)
client.loop_start()
irlast=0
while (True):
        card_data = rfid.read()
        if card_data != None:
                print(card_data.hex())
                berryclip.setYellowLED(1)
                print("got data")
                data = {'roomId': roomId, 'RFID': card_data.hex(), 'command': 'cardask'}
                client.publish('/fk/rr', json.dumps(data))
                card_data=None
                time.sleep(2)

