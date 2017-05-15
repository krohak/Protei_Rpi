import paho.mqtt.client as mqtt
import sys
# This is the Publisher

client = mqtt.Client()
client.connect("iot.eclipse.org",1883,60)
client.publish("TOPIC", sys.argv[1]);
client.disconnect();


