network="1234"

echo "Switching on Wi-Fi"
#sudo ifconfig wlan0 up

echo "Finding network $network"
a="`sudo iwlist wlan0 scan | grep $network`"

if [ $a ]
then
	echo $a
	echo "Found network $network"
	echo "Connecting..."
	#sudo iwconfig wlan0 essid $network key s:password
	#sudo dhclient wlan0
	echo "Sending Data through $network"
	python send_data.py $1 $2 2
	echo "Data Sent"
	echo "Disconnecting Wi-Fi"
	#sudo ifconfig wlan0 down
else
	echo "Not found network $network"
	echo "Disconnecting Wi-Fi"
  #sudo ifconfig wlan0 down
	echo "Switching on Mobile Data"
	echo "Sending data to server using Mobile Data"
	python send_data.py $1 $2 1
	echo "Data Sent"
	echo "Disconnecting Mobile Data"
fi
