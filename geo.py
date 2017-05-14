from geojson import Feature, Point, Polygon
import json
import sys
import paho.mqtt.client as mqtt
import hmac


hostname = "iot.eclipse.org" # Sandbox broker
port = 1883 # Default port for unencrypted MQTT

topic="TOPIC1"
topic2="TOPIC2"


def on_connect(client, userdata, rc):
	# Successful connection is '0'
	print("Connection result: " + str(rc))
	if rc == 0:
		# Subscribe to topics
		client.subscribe(topic)
		client.subscribe(topic2)

def on_message(client, userdata, message):
	#print("Received message on %s: %s (QoS = %s)" %
		#(message.topic, message.payload.decode("utf-8"), str(message.qos)))

	if(message.topic=="TOPIC1"):
		recv=message.payload.decode("utf-8")
		hash=recv.split('_')[0]
		to_hash=recv.split('_')[1]

		digest_maker = hmac.new('PASSWORD')
		digest_maker.update(to_hash)
		digest = digest_maker.hexdigest()

		if(digest==hash):
			print "ok"
			packet=json.loads(to_hash)
			print(hash)
			print(packet)


			prop=packet["properties"]
			coord=tuple(packet["coordinates"])

			my_feature = Feature(geometry=Point(coord),properties=prop)


			with open('protei.geojson') as f:
				data = json.load(f)
			data['features'].append(my_feature)

			with open('protei.geojson', 'w') as f:
    				json.dump(data, f)

		else:
			print "Data integrity check failed"
			print "Hash value: %s"%(hash)
			print "Computer Value: %s"%(digest)
	

	elif(message.topic=="TOPIC2"):
		recv=message.payload.decode("utf-8")
		hash=recv.split('_')[0]
		to_hash=recv.split('_')[1]

		digest_maker = hmac.new('PASSWORD')
                digest_maker.update(to_hash)
                digest = digest_maker.hexdigest()

                if(digest==hash):
                        print "ok"
                        packet=json.loads(to_hash)
                        #print(hash)
                        print(type(packet["coordinates"]))
			cord_list=[packet["coordinates"]]+[[[0,0]]]
			print(cord_list)


			prop=packet["properties"]
                        coord=tuple(cord_list)

                        my_feature = Feature(geometry=Polygon(coord),properties=prop)
			print(my_feature)





def on_disconnect(client, userdata, rc):
	if rc != 0:
		print("Disconnected unexpectedly")


# Initialize client instance
client = mqtt.Client()

# Bind events to functions
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to the specified broker
client.connect(hostname, port=port)

# Network loop runs in the background to listen to the events
client.loop_forever()

'''22.28397,114.11993
22.28814,114.12705
22.28876,114.09847
22.282231,114.129151
'''

