import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import json
import GPIOhardware.hardware as hardware
import GPIOhardware.rfid as rfid
import GPIOhardware.berryclip as berryclip
from tasks import runTasks


roomId=1
## Main. 
def on_message(client, userdata, msg):
        print(msg.payload)
        data = json.dumps(str(msg.payload))[2:-1]
    print(data)
    if data[-1]['type']=='cardAsked':
        berryclip.setYellowLED(0)
        if data[-1]['response']=='confirmed' or data[-1]['response']=='booked':
            berryclip.setGreenLED(1)
        if data[-1]['response']=='denied':
            berryclip.setRedLED(1)

def on_connect(client, userdata, flags, rc):
    print(("connected with result code " + str(rc)))
    client.subscribe("/fk/rr/2")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("iot.eclipse.org", 1883, 60)
client.loop_start()
while (True):
        card_data = rfid.read()
        if card_data != None:
            print("got data")
            data = {'roomId': roomId, 'RFID': card_data.hex(), 'command': 'cardask'}
            client.publish('/fk/rr', json.dumps(data))
            card_data=None
            time.sleep(2)


#try: 
	#runTasks()



	## todo: 
	# insert server communication in this code. not my task to create; will wait for usable functions. 		
	# rfid shall also handle instant-booking. 
	# what happens when one scans card again after logged in?
	# create a clearer state-machine view. (same behaviour)


	
	#GPIO.cleanup()
	#hardware.close()
	
#except KeyboardInterrupt: 
        #GPIO.cleanup()
	#hardware,close()
	#print("bye")


