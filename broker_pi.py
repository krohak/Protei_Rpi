from __future__ import print_function
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import hmac
import json

count=0 #everytime it receive data from other boat, it will go up. If it receives 3, it will resets
max=3 #Threshold value


hostname = "iot.eclipse.org"
topic_near="krohak/near"
port=1883

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("CHANNEL1")

def on_connect2(client, userdata, rc):
  print("Connected with result code2 "+str(rc))
  client.subscribe("CHANNEL2")


def on_message(client, userdata, msg):
	if(msg.topic=="CHANNEL1"):
		hash=(msg.payload.decode("utf-8")).split("_")[0]
		print(("Received Hash: %s")%(hash))
		data=(msg.payload.decode("utf-8")).split("_")[1]
		digest_maker = hmac.new('PASSWORD') #for validating the data from a specific. We could have different passwords for each sensor in the network
        	digest_maker.update(data)
		digest = digest_maker.hexdigest() #if hexdigest of the unit and the one of the server match, it will process the data
		print(("Computed Hash: %s")%(digest))


		if digest == hash:
			print("Valid data")
			with open('log.json', 'a') as f:
				print(data,file=f)
			global count
			count+=1
			print(count)
		else:
			print("Invalid data")

	

def on_message2(client, userdata, msg):
	if(msg.topic=="CHANNEL2"):
		print(("Received new threshold value: %s")%msg.payload.decode("utf-8"))
		try:
			global max
			max=int(msg.payload.decode("utf-8"))
		except Exception,e:
			print(e)
	
    
client = mqtt.Client()
client2 = mqtt.Client()
client.connect("localhost",1883,60)
client2.connect("iot.eclipse.org",1883)

client.on_connect = on_connect
client.on_message = on_message

client2.on_connect = on_connect2
client2.on_message = on_message2


#client.loop_start()

while True:
	client.loop_start()
	client2.loop_start()
	time.sleep(2)
	global max
	if count>=max:
		client.loop_stop()
		client2.loop_stop()
		cord_list=[]
		avg_temp=0
		avg_hum=0
		avg_pres=0
		f=open('log.json','r+')
		for a in f:
			packet=json.loads(a)
			cord_list+=[packet["coordinates"]]
			avg_temp+=packet["properties"]["Temperature"]
			avg_hum+=packet["properties"]["Humidity"]
			avg_pres+=packet["properties"]["Pressure"]
		avg_temp/=count
		avg_hum/=count
		avg_pres/=count
		qstr=('{"coordinates":%s,"properties":{"Temperature":%s,"Pressure":%s,"Humidity":%s}}'%(cord_list,avg_temp,avg_pres,avg_hum))
		print(qstr) #Average 
		digest_maker = hmac.new('PASSWORD')
		digest_maker.update(qstr)
		digest = digest_maker.hexdigest()
		
		to_send=digest+'_'+qstr
		try:
			publish.single(topic_near, payload=str(to_send),
                	qos=1,
                	hostname=hostname,
                	port=port)
			f.seek(0)
			f.truncate()
			f.close()
			count=0
			print("Data sent")
		except Exception,e:
			print(e)
	time.sleep(2)
