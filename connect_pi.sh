echo "Switching on Wi-Fi"
#sudo ifconfig wlan0 up

echo "Finding network $1"
a="`sudo iwlist wlan0 scan | grep $1`"

if [ $a ]
then
	echo $a
	echo "Found network $1"
	echo "Connecting..."
	#sudo iwconfig wlan0 essid $1 key s:password
	#sudo dhclient wlan0
	echo "Sending Data through $1"
	python send_data.py 114 22 2
	echo "Data Sent"
	echo "Disconnecting Wi-Fi"
	#sudo ifconfig wlan0 down
else
	echo "Not found network $1"
	echo "Disconnecting Wi-Fi"
  #sudo ifconfig wlan0 down
	echo "Switching on Mobile Data"
	echo "Sending data to server using Mobile Data"
	python send_data.py 114 22 1
	echo "Data Sent"
	echo "Disconnecting Mobile Data"
fi
