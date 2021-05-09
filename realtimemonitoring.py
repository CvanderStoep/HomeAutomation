import requests  # , json
import time
from influxdb import InfluxDBClient
from datetime import datetime, timedelta

from phue import Bridge

computer_adress = 'localhost'  # where is InfluxDB installed
computer_port = 8086  # port number of the DB
client = InfluxDBClient(host=computer_adress, port=computer_port)
database_name = 'localdata'


def initbridge():
    global bridge
    from private_info import ip_adress_hue_bridge
    bridge = Bridge(ip_adress_hue_bridge)  # connected to Deco mesh
    bridge.connect()  # this command is needed only once; press hue bridge button en run bridge.connect() command.
    return


def getsensors(sensortype):
    # get a flat list of sensor objects of type sensortype
    sensors = bridge.sensors
    print()
    print('Output for selected sensors:')

    for sensor in sensors:
        if sensortype in sensor.name:
            print(sensor.sensor_id, sensor.name, sensor.state)

    # get a dictionary with sensor id as key
    sensors = bridge.get_sensor_objects('id')
    temp_sensor_second_floor = sensors[8].state['temperature'] / 100
    temp_sensor_ground_floor = sensors[17].state['temperature'] / 100
    temp_sensor_first_floor = sensors[75].state['temperature'] / 100  # temp in degC

    print()
    print('Temperature Sensor[8] - second_floor: ', temp_sensor_second_floor)
    print('Temperature Sensor[17] - ground_floor: ', temp_sensor_ground_floor)
    print('Temperature Sensor[75] - first_floor: ', temp_sensor_first_floor)
    return


def getoutsideweather(city="Delft"):
    # from private_info import complete_url  # combines api key and city for the temperature
    from private_info import web_url
    complete_url = web_url + city
    response = requests.get(complete_url)
    x = response.json()
    y = x["main"]
    current_temperature = round(y["temp"] - 273.15, 2)  # convert K to deg C
    return current_temperature


if __name__ == '__main__':

    print(client.get_list_database())
    # print(client.query(database=database_name, query='select * from temperature'))

    """" 
    get data from the HUE
    """
    initbridge()

    cities = ["Delft", "London", "Maastricht", "Sydney", "Amsterdam"]
    while True:
        data_point = []
        for city in cities:
            temp_outside = getoutsideweather(city)  # get the current outside Temperature using OpenWeatherData
            data_point = data_point + \
                         [{'measurement': 'temperature',
                           'tags': {'location': city},
                           'fields': {'temperature': temp_outside}
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

        client.write_points(data_point, database=database_name)
        print(datetime.now(), data_point)
        time.sleep(60)  # sleep time in sec.
