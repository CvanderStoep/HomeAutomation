#
# Get live data from the following sources:
# -City weather data using openweathermap api
# -Hue light sensor data
# -Hue temperature sensor data
# -Solarpanel data
#
# Output is send to InfluxDB
# Output is visualized using Grafana
#


import time
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from initbridge import initbridge
from get_hue_temp import hue_temp
from get_hue_lights import hue_lights
from get_outside_weather import outside_weather
from private_info import cities
from private_info import database_name
from private_info import computer_address
from private_info import computer_port

from InverterExport import InverterExport

client = InfluxDBClient(host=computer_address, port=computer_port)  # connect to Influx 1.8 DB
inverter_exporter = InverterExport('config.cfg')  # connect to the solar inverter

retention_policy_default = None  # the temperature readings are stored indefinitely
retention_policy_one_week = "one-week"  # the light readings are stored one week

if __name__ == '__main__':

    print(client.get_list_database())
    results = (client.query(database=database_name, query='select * from temperature limit 5'))
    for result in list(results.get_points()):
        print(result)

    # connect to hue bridge
    bridge = initbridge()
    print(bridge.username)
    while True:
        # get outside weather data from the various cities using open weather site
        data_point = []
        for city in cities:
            data_point = data_point + outside_weather(city)

        client.write_points(data_point, database=database_name, retention_policy=retention_policy_default)
        print(datetime.now(), data_point)

        # get inside temperature data from the hue bridge
        data_point = hue_temp(bridge)
        client.write_points(data_point, database=database_name, retention_policy=retention_policy_default)
        print(datetime.now(), data_point)

        # get status of the lights from the hue
        data_point = hue_lights(bridge)
        client.write_points(data_point, database=database_name, retention_policy=retention_policy_one_week)
        print(datetime.now(), data_point)

        # get data from the solar inverter
        inverter_exporter.run()

        time.sleep(60)  # sleep time in sec.
