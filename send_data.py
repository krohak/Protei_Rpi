import paho.mqtt.publish as publish
import sys
import datetime
import hmac
from sense_hat import SenseHat

sense = SenseHat()

port = 1883 # Default port for unencrypted MQTT


x_cord=float(sys.argv[1])
y_cord=float(sys.argv[2])

print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])

def get_details():
	if(sys.argv[3]=="1"):
                hostname = "iot.eclipse.org" # Sandbox broker
                topic_far="TOPIC1"
		return hostname,topic_far
        elif(sys.argv[3]=="2"):
                hostname = "192.168.1.1"
                topic_far="TOPIC2"
		return hostname,topic_far

try:

	device="DEVICE#"
	#coord=[114.102757,22.280894]
	coord=[x_cord,y_cord]
        humidity = str(sense.get_humidity())
        #print(humidity)
        temp = str(sense.get_temperature())
        #print(temp)
        pressure = str(sense.get_pressure())
        #print(pressure)
        north = str(sense.get_compass())
        #print(north)
	date=str(datetime.datetime.now())
        #print(date)

	qstr=('{"coordinates":%s,"properties":{"Device":%s,"Time":"%s","Temperature":%s,"Pressure":%s,"Humidity":%s,"Magnetometer":%s}}'%(coord,device,date,temp,pressure,humidity,north))

	digest_maker = hmac.new('PASSWORD')
	digest_maker.update(qstr)
	
	digest = digest_maker.hexdigest()
	print(digest)
	
	to_send=digest+'_'+qstr
	#to_send="digest"+'_'+qstr
	
	hostname,topic_far=get_details()


	print(hostname)
	print(topic_far)
	publish.single(topic_far, payload=str(to_send),
                qos=1,
                hostname=hostname,
                port=port)

	
	print(to_send)


except Exception,e:
        print("failed")
        print(e)
        sys.exit(1)

