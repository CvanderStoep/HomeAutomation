# Home Automation Project 
(HUE, INFLUXDB, SOLARPANEL, GRAFANA, DOCKER, DOCKER COMPOSE)
### Get live data from the following sources:
* City weather data using openweathermap api
* Hue light sensor data
* Hue temperature sensor data
* Solarpanel data from Inverter

### Output is send to InfluxDB
### Output is visualized using Grafana

### Working on: 
* Publishing all via Docker Containers for InfluxDB, (Python) & Grafana
* Issue with Hue bridge and python code in a docker (needs to authenticate every time)
