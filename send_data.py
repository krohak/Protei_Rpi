import paho.mqtt.publish as publish
import sys
import datetime
from sense_hat import SenseHat

sense = SenseHat()

hostname = "iot.eclipse.org" # Sandbox broker
port = 1883 # Default port for unencrypted MQTT

topic_time = "TIME"
topic_hum = "HUM"
topic_temp = "TEMP"
topic_pres = "PRES"
topic_nor = "NOR"

try:



        humidity = str(sense.get_humidity())
        print(humidity)
        publish.single(topic_hum, payload=humidity,
        	qos=1,
        	hostname=hostname,
        	port=port)

        temp = str(sense.get_temperature())
        print(temp)
        publish.single(topic_temp, payload=temp,
        	qos=1,
        	hostname=hostname,
        	port=port)

        pressure = str(sense.get_pressure())
        print(pressure)
        publish.single(topic_pres, payload=pressure,
        	qos=1,
        	hostname=hostname,
        	port=port)

        north = str(sense.get_compass())
        print(north)
        publish.single(topic_nor, payload=north,
        	qos=1,
        	hostname=hostname,
        	port=port)

        date=str(datetime.datetime.now())
        print(date)
        publish.single(topic_time, payload=date,
        	qos=1,
        	hostname=hostname,
        	port=port)





except Exception,e:
        print("failed")
        print(e)
        sys.exit(1)
