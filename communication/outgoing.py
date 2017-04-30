import paho.mqtt.client as mqtt
import json

import software.LEDs as LEDs
import data.roomData as roomData



def send_message (roomID, card_data, commandType):
        print("out.send")
        LEDs.setYellow(1)
        data = {'roomId': roomID, 'RFID': card_data.hex(), 'command': commandType}
        client.publish(roomData.CHANNEL_PUB, json.dumps(data))



client=mqtt.Client()
#client.on_connect = on_connect
#client.on_message = on_message

client.connect(roomData.CHANNEL_CONNECT, 1883, 60)
client.loop_start()



