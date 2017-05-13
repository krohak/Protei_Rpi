import paho.mqtt.publish as publish
import sys
import datetime
import hmac
from sense_hat import SenseHat

sense = SenseHat()
digest_maker = hmac.new('PASSWORD')

hostname = "iot.eclipse.org" # Sandbox broker
port = 1883 # Default port for unencrypted MQTT

topic_far="TOPIC"

try:

	device="DEVICE#"
	coord=[114.12915,22.282231]
        humidity = str(sense.get_humidity())
        print(humidity)
        temp = str(sense.get_temperature())
        print(temp)
        pressure = str(sense.get_pressure())
        print(pressure)
        north = str(sense.get_compass())
        print(north)
	date=str(datetime.datetime.now())
        print(date)

	qstr=('{"coordinates":%s,"properties":{"Device":%s,"Time":"%s","Temperature":%s,"Pressure":%s,"Humidity":%s,"Magnetometer":%s}}'%(coord,device,date,temp,pressure,humidity,north))

	digest_maker.update(qstr)
	
	digest = digest_maker.hexdigest()
	print(digest)
	
	to_send=digest+'_'+qstr
	#to_send="digest"+'_'+qstr
	
	publish.single(topic_far, payload=str(to_send),
                qos=1,
                hostname=hostname,
                port=port)

	
	print(to_send)


except Exception,e:
        print("failed")
        print(e)
        sys.exit(1)

