# Protei_Rpi

![](https://c1.staticflickr.com/3/2822/34294204205_b1a6fc9184_b.jpg)
![](https://c1.staticflickr.com/5/4158/34253978676_6f72a60dfc_b.jpg)

### connect_pi.sh 
    Shell Script to manage Wi-Fi connection
    - Takes in the coordinates as two arguments 
    - Wi-Fi ESSID hardcoded
    - Checks if Wi-Fi with a specific ESSID is available
    - If yes, connect to it and send the data to broker Pi
    - If no, connect to mobile data and send data to the server

### send_data.py
    Python Script for sending out the Data
    - Takes x_coordinate,y_coordinate and an Int as an argument
    - Int decides where to send out the data [ Server (1) / Router (2)]
    - Data: Coordinates, Device ID, Time, Temperature, Pressure, Humidity, Magnetometer
    - Computes the MAC of the data and sends it along

### broker_pi.py
    Python Script for the broker Pi
    First Client:
    - Listens on a specific MQTT channel
    - Computes MAC, checks it against the data
    - Stores the data from three Rpis on log.json
    - After receiving data from three Rpis, AGGREGATES DATA
        - computes average of temperature, pressure, humidity
    - Sends it off to the server on a different channel
    - Truncates log.json, resets counter
    Second Client:
    - Receives data in the form of an integer from the server
    - Updates the threshold value of the number of JSON strings to be aggregated and sent back to the server

### geo.py
    Python Script for the Server [AWS]
    - Listens to feed on two MQTT channels
        - For data directly sent to the server from non-router Pis
        - For aggregated data sent from router Pis
    - Checks for data integrity by computing the MAC and verifying against sent MAC
    - Stores the data in protei.geojson or neighborhoods.geojson according to where the data is received from

### update_threshold.py
    Python Script to update the threshold value on the broker Pi
    - Takes int as argument
    - Updates the specific feed for the broker to listen to

### geojs.html
    HTML file for plotting GeoJSON data using Leaflet
    - Displays data from 'protei.geojson' as Markers
    - Displays data from 'neighborhoods.geojson' as Polygon (Choropleth Map)
    - leaflet.markercluster.js, MarkerCluster.css for aesthetics

![](https://c1.staticflickr.com/3/2846/33452617874_d067a5c853_b.jpg)
![](https://c1.staticflickr.com/5/4175/33452619374_47e23333da_b.jpg)
