from geojson import Feature, Point
import json
import socket
import sys

mysock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
       	sk=('IP',1234);
        
	mysock.bind(sk)
except socket.error:
        print("failed")
        sys.exit(1)

mysock.listen(5)
while True:
    conn,addr=mysock.accept()
    data=conn.recv(1000)
    if not data:
        break

    #print((data))
    mylist = str(data).split(',')
    #print(mylist)
    date=mylist[0]
    temp=mylist[1]
    pressure=mylist[2]
    humidity=mylist[3]
    north=mylist[4]
    #print(date)

    packet={"Time":date,"Temperature":temp,"Pressure":pressure,"Humidity":humidity,"Magnetometer":north}
    print(packet)
    #conn.sendall(data)
    #data=conn.recv(20)
    #print("%s\n"%(data))

    #'''
    my_feature = Feature(geometry=Point((114,22)),properties=(packet))
    #my_feature = Feature(geometry=Point((114.135421,22.283063)),properties=(packet))
    '''22.28397,114.11993
22.28814,114.12705

22.28876,114.09847

22.282231,114.129151'''

    with open('protei.geojson') as f:
        data = json.load(f)

    data['features'].append(my_feature)

    with open('protei.geojson', 'w') as f:
        json.dump(data, f)
    #'''

conn.close()
mysock.close()