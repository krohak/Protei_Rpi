from __future__ import print_function
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import hmac
import json

count=0

hostname = "iot.eclipse.org"
topic_near="TOPIC"
port=1883

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("TOPIC")

def on_message(client, userdata, msg):
	hash=(msg.payload.decode("utf-8")).split("_")[0]
	data=(msg.payload.decode("utf-8")).split("_")[1]
	digest_maker = hmac.new('PASSWORD')
        digest_maker.update(data)
	digest = digest_maker.hexdigest()


	if digest == hash:
		print("Valid data")
		with open('log.json', 'a') as f:
			print(data,file=f)
		global count
		count+=1
		print(count)
	
    
client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

#client.loop_start()

while True:
	client.loop_start()
	time.sleep(2)
	'''
	no=0
	with open('log.json') as f:
		no=(sum(1 for _ in f))
		print(no)
	'''
	if count>=3:
		client.loop_stop()
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
		avg_temp/=3
		avg_hum/=3
		avg_pres/=3
		qstr=('{"coordinates":%s,"properties":{"Temperature":%s,"Pressure":%s,"Humidity":%s}}'%(cord_list,avg_temp,avg_pres,avg_hum))
		print(qstr)
		digest_maker = hmac.new('PASSWORD')
		digest_maker.update(qstr)
		digest = digest_maker.hexdigest()
		
		to_send=digest+'_'+qstr
		publish.single(topic_near, payload=str(to_send),
                qos=1,
                hostname=hostname,
                port=port)
		f.seek(0)
		f.truncate()
		f.close()
		count=0
	#lastly
	print("done")
	time.sleep(2)
