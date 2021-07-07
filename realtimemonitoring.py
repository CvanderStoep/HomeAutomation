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
from outsideweather import getoutsideweather
from private_info import database_name
from private_info import computer_address
from private_info import computer_port

from InverterExport import InverterExport

client = InfluxDBClient(host=computer_address, port=computer_port)
inverter_exporter = InverterExport('config.cfg')

retention_policy_default = None  # the temperature readings are stored indefinitely
retention_policy_one_week = "one-week"  # the light readings are stored one week

# def initbridge():
#     global bridge
#     from private_info import ip_address_hue_bridge
#     bridge = Bridge(ip_address_hue_bridge)  # connected to Deco mesh
#     bridge.connect()  # this command is needed only once; press hue bridge button en run bridge.connect() command.
#     return


# def getoutsideweather(city="Delft"):
#     # from private_info import complete_url  # combines api key and city for the temperature
#     from private_info import web_url
#     complete_url = web_url + city
#     response = requests.get(complete_url)
#     x = response.json()
#     y = x["main"]
#     wind_speed = x["wind"]["speed"]
#     wind_direction = x["wind"]["deg"]
#     current_temperature = round(y["temp"] - 273.15, 2)  # convert K to deg C
#     weather_type = x["weather"][0]["main"]
#     humidity = x["main"]["humidity"]
#     pressure = x["main"]["pressure"]
#     return current_temperature, wind_speed, weather_type, humidity, pressure, wind_direction


if __name__ == '__main__':

    print(client.get_list_database())
    results = (client.query(database=database_name, query='select * from temperature limit 5'))
    for result in list(results.get_points()):
        print(result)

    """" 
    get data from the HUE
    """
    bridge = initbridge()

    cities = ["Delft", "London", "Maastricht", "Sydney", "Amsterdam", "Schiermonnikoog", "De Bilt", "Caen", "Delfgauw"]

    while True:
        data_point = []
        for city in cities:
            temp_outside, wind_speed, weather_type, humidity, pressure, wind_direction = \
                getoutsideweather(city)  # get the current outside Temperature using OpenWeatherData
            data_point = data_point + \
                         [{'measurement': 'temperature',
                           'tags': {'location': city},
                           'fields': {'temperature': temp_outside}
                           }] + \
                         [{'measurement': 'pressure',
                           'tags': {'location': city},
                           'fields': {'pressure': pressure}
                           }] + \
                         [{'measurement': 'humidity',
                           'tags': {'location': city},
                           'fields': {'humidity': humidity}
                           }] + \
                         [{'measurement': 'weather_type',
                           'tags': {'location': city},
                           'fields': {'weather_type': weather_type}
                           }] + \
                         [{'measurement': 'wind',
                           'tags': {'location': city},
                           'fields': {'direction': wind_direction}
                           }] + \
                         [{'measurement': 'wind',
                           'tags': {'location': city},
                           'fields': {'speed': wind_speed}
                           }]

        sensors = bridge.get_sensor_objects('id')
        temp_sensor_first_floor = sensors[75].state['temperature'] / 100  # temp in degC
        temp_sensor_ground_floor = sensors[17].state['temperature'] / 100
        temp_sensor_second_floor = sensors[8].state['temperature'] / 100

        print()
        print('Temperature Sensor[8] - second_floor: ', temp_sensor_second_floor)
        print('Temperature Sensor[17] - ground_floor: ', temp_sensor_ground_floor)
        print('Temperature Sensor[75] - first_floor: ', temp_sensor_first_floor)

        data_point = data_point + \
                     [{'measurement': 'hue_temperature',
                       'tags': {'sensor': "ground_floor"},
                       'fields': {'temperature': temp_sensor_ground_floor}
                       }]
        data_point = data_point + \
                     [{'measurement': 'hue_temperature',
                       'tags': {'sensor': "first_floor"},
                       'fields': {'temperature': temp_sensor_first_floor}
                       }]
        data_point = data_point + \
                     [{'measurement': 'hue_temperature',
                       'tags': {'sensor': "second_floor"},
                       'fields': {'temperature': temp_sensor_second_floor}
                       }]

        client.write_points(data_point, database=database_name, retention_policy=retention_policy_default)
        print(datetime.now(), data_point)

        data_point = []
        lights = bridge.lights
        for light in lights:
            if light.on:
                light_on = 1
            else:
                light_on = 0
            data_point = data_point + \
                         [{'measurement': 'hue_lights',
                           'tags': {'light': light.name},
                           'fields': {'on': light_on}
                           }]

        client.write_points(data_point, database=database_name, retention_policy=retention_policy_one_week)

        print(datetime.now(), data_point)
        inverter_exporter.run()

        time.sleep(60)  # sleep time in sec.
