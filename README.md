# Protei_Rpi

![](https://c1.staticflickr.com/3/2822/34294204205_b1a6fc9184_b.jpg)
![](https://c1.staticflickr.com/5/4158/34253978676_6f72a60dfc_b.jpg)

1) connect_pi.sh 
    
    Shell Script to manage Wi-Fi connection
    - Takes in the coordinates as two arguments 
    - Wi-Fi ESSID hardcoded

2) send_data.py

    Python Script for sending out the Data
    - Takes x_coordinate,y_coordinate and an Int as an argument
    - Int decides where to send out the data [ Server (1) / Router (2)]
    - Computes the MAC of the data and sends it along

3) broker_pi.py

    Python Script for the broker Pi
    - Listens on a specific MQTT channel
    - Computes MAC, checks it against the data
    - Stores the data from three Rpis on log.json
    - After receiving data from three Rpis, AGGREGATES DATA
        - computes average of temperature, pressure, humidity
    - Sends it off to the server on a different channel
    - Truncates log.json, resets counter

4) geo.py

    Python Script fot the Server [AWS]
    - Listens to feed on two MQTT channels
        - For data directly sent to the server from non-router Pis
        - For aggregated data sent from router Pis
    - Checks for data integrity by computing the MAC and verifying against sent MAC
    - Stores the data in protei.geojson or neighborhoods.geojson according to where the data is received from

5) geojs.html

    HTML file for plotting GeoJSON data using Leaflet
    - Displays data from 'protei.geojson' as Markers
    - Displays data from 'neighborhoods.geojson' as Polygon (Choropleth Map)
    - leaflet.markercluster.js, MarkerCluster.css for aesthetics

![](https://c1.staticflickr.com/3/2846/33452617874_d067a5c853_b.jpg)
![](https://c1.staticflickr.com/5/4175/33452619374_47e23333da_b.jpg)
