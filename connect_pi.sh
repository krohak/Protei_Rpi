echo "Switching on Wi-Fi"
sudo ifconfig wlan0 up


echo "Finding network $1"
a="`sudo iwlist wlan0 scan | grep $1`"

if [ $a ]
then
	echo $a
	echo "Found network $1"
	echo "Connecting..."
	sudo iwconfig wlan0 essid $1 key s:password
	sudo dhclient wlan0
	echo "Sending Data through $1"
	sudo ping -i 1 www.google.com 
	echo "Data Sent"
	echo "Disconnecting Wi-Fi"
	sudo ifconfig wlan0 down	
else
	echo "Not found network $1"
	echo "Disconnecting Wi-Fi"
        sudo ifconfig wlan0 down
	echo "Sending data to server using mobile data"

fi