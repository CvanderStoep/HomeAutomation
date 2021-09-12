#
# Get live data from the following sources:
# -City weather data using openweathermap api
#
# Output is send to InfluxDB
# Output is visualized using Grafana
# Use is made of 3 docker containers: InfluxDB, Grafana, this python file
#


import time
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from get_outside_weather import outside_weather
from private_info import cities
from private_info import database_name
from private_info import docker_address
from private_info import computer_port

time.sleep(5)
client = InfluxDBClient(host=docker_address, port=computer_port)  # connect to Influx 1.8 DB

retention_policy_default = None  # the temperature readings are stored indefinitely
retention_policy_one_week = "one-week"  # the light readings are stored one week

if __name__ == '__main__':

    print(client.get_list_database())
    results = (client.query(database=database_name, query='select * from temperature limit 5'))
    for result in list(results.get_points()):
        print(result)


    while True:
        # get outside weather data from the various cities using open weather site
        data_point = []
        for city in cities:
            data_point = data_point + outside_weather(city)

        client.write_points(data_point, database=database_name, retention_policy=retention_policy_default)
        print(datetime.now(), data_point)


        time.sleep(60)  # sleep time in sec.
