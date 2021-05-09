import requests  # , json
# from time import sleep
import time
from influxdb import InfluxDBClient
from datetime import datetime, timedelta

computer_adress = 'localhost'  # where is InfluxDB installed
computer_port = 8086  # port number of the DB
client = InfluxDBClient(host=computer_adress, port=computer_port)
database_name = 'localdata'


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

    cities = ["Delft", "London", "Maastricht", "Sydney"]
    while True:
        data_point = []
        for city in cities:
            temp_outside = getoutsideweather(city)  # get the current outside Temperature using OpenWeatherData
            data_point = data_point + \
                         [{'measurement': 'temperature',
                           'tags': {'location': city},
                           'fields': {'temperature': temp_outside}
                           }]

        client.write_points(data_point, database=database_name)
        print(datetime.now(), data_point)
        time.sleep(60)  # sleep time in sec.
