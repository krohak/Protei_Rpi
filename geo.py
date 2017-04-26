from geojson import Feature, Point
import json
import sys
import paho.mqtt.client as mqtt

date=""
temp=""
pressure=""
humidity=""
north=""
data=""

hostname = "iot.eclipse.org" # Sandbox broker
port = 1883 # Default port for unencrypted MQTT

topic = "krohak/#"
topic_time = "krohak/test/time"
topic_hum = "krohak/test/hum"
topic_temp = "krohak/test/temp"
topic_pres = "krohak/test/pres"
topic_nor = "krohak/test/nor"

def on_connect(client, userdata, rc):
        # Successful connection is '0'
        print("Connection result: " + str(rc))
        if rc == 0:
                # Subscribe to topics
                client.subscribe(topic)

def on_message(client, userdata, message):
        print("Received message on %s: %s (QoS = %s)" %
                (message.topic, message.payload.decode("utf-8"), str(message.qos)))
        if(message.topic==topic_hum):
                global humidity
                humidity=message.payload.decode("utf-8")
                print(humidity)
        elif(message.topic==topic_temp):
                global temp
                temp=message.payload.decode("utf-8")
                print(temp)
        elif(message.topic==topic_pres):
                global pressure
                pressure=message.payload.decode("utf-8")
                print(pressure)
        elif(message.topic==topic_nor):
                global north
                north=message.payload.decode("utf-8")
                print(north)
        elif(message.topic==topic_time):
                global date
                date=message.payload.decode("utf-8")
                print(date)

                packet={"Time":date,"Temperature":temp,"Pressure":pressure,"Humidity":humidity,"Magnetometer":north}
                print(packet)


                my_feature = Feature(geometry=Point((114.234,22.76543)),properties=(packet))
                #my_feature = Feature(geometry=Point((114.135421,22.283063)),properties=(packet))

                with open('protei.geojson') as f:
                        data = json.load(f)
                data['features'].append(my_feature)

                with open('protei.geojson', 'w') as f:
                        json.dump(data, f)


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


'''114.11993,22.28397
114.12705,22.28814
114.09847,22.28876
114.12915,22.282231

'''
