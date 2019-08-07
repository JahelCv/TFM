import paho.mqtt.client as mqtt #import the client1
import time
############
def on_message(client, userdata, message):
    print("ON_MESSAGE!")
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################
#broker_address="192.168.1.184"
broker_address="iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("P1", clean_session=True) #create new instance
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address) #connect to broker
client.loop_start() #start the loop

#print("Subscribing to topic","house/bulbs/bulb1")
#client.subscribe("house/bulbs/bulb1")
print("Subscribing to topic","house/main-luzjahel")
client.subscribe("house/main-luzjahel")

#print("Publishing message to topic","house/main-luzjahel")
#client.publish("house/main-luzjahel","Estic gastant pahomqtt")

time.sleep(60) # wait
client.loop_stop() #stop the loop