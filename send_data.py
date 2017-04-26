import socket
import sys
import datetime
from sense_hat import SenseHat

sense = SenseHat()

mysock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
        ainfo=socket.getaddrinfo("IP",1234)
        
        mysock.connect(ainfo[0][4])
        date=str(datetime.datetime.now())
        print(date)
        #mysock.sendall(date)
        humidity = str(sense.get_humidity())
        print(humidity)
        #mysock.sendall(humidity)
        temp = str(sense.get_temperature())
        print(temp)
        #mysock.sendall(temp)
        pressure = str(sense.get_pressure())
        print(pressure)
        #mysock.sendall(pressure)
        north = str(sense.get_compass())
        print(north)
	#mysock.sendall(north)

	#properties={"Time":"","Temperature":"","Pressure":"","Humidity":"","Magnetometer":""})
        #packet=str('"Time":"'+date+'",'+'"Temperature":"'+temp+'",'+'"Pressure":"'+pressure+'",'+'"Humidity":"'+humidity+'",'+'"Magnetometer":"'+north+'"').encode()

	

        packet=str(date+","+temp+","+pressure+","+humidity+","+north).encode()
        mysock.sendall(packet)


except socket.error:
        print("failed")
        sys.exit(1)



mysock.close()

