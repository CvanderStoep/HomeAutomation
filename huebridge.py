""""
documentation can be found at below link:
https://github.com/studioimaginaire/phue

"""
from phue import Bridge
import pandas as pd
from pathlib import Path
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import requests, json

DATA_FILE = 'hue_data.csv'


def initbridge():
    global bridge
    from private_info import ip_adress_hue_bridge
    bridge = Bridge(ip_adress_hue_bridge)  # connected to Deco mesh
    bridge.connect()  # this command is needed only once; press hue bridge button en run bridge.connect() command.
    return


def getdictionary():
    # returns a full dictionary
    huedictionary = bridge.get_api()
    print('Output full dictionary of Hue Bridge:')
    for x, y in huedictionary.items():
        print(x, y)
    return


def getlights():
    # get a flat list of light objects
    lights = bridge.lights
    print()
    print()
    print('Output for all lights:')
    for light in lights:
        print(light.light_id, light.name, light.on, light.brightness, light.type)

    return


def getsensors(sensortype):
    # get a flat list of sensor objects of type sensortype
    sensors = bridge.sensors
    print()
    print('Output for selected sensors:')

    for sensor in sensors:
        if (sensortype in sensor.name):
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


def getoutsideweather():
    from private_info import complete_url  # combines api key and city for the temperature
    response = requests.get(complete_url)
    x = response.json()
    y = x["main"]
    current_temperature = round(y["temp"] - 273.15, 2)  # convert K to deg C
    return current_temperature


def update(frame):
    # activate the sensors and get the data
    sensors = bridge.get_sensor_objects('id')
    temp_sensor_first_floor = sensors[75].state['temperature'] / 100  # temp in degC
    temp_sensor_ground_floor = sensors[17].state['temperature'] / 100
    temp_sensor_second_floor = sensors[8].state['temperature'] / 100
    temp_outside = getoutsideweather()  # get the current Temperature in outside using OpenWeatherData

    # add new time and sensor temperature data to a .csv file
    new_data = {'DateTime': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'T_first_floor': [temp_sensor_first_floor],
                'T_ground_floor': [temp_sensor_ground_floor],
                'T_second_floor': [temp_sensor_second_floor],
                'T_outside': [temp_outside]}
    newdf = pd.DataFrame(new_data)  # only the latest data
    newdf.to_csv(DATA_FILE, mode='a', header=False)
    print(new_data)
    # print('T-second_floor last update: ', sensors[8].state['lastupdated'])

    time_data.append(datetime.now())
    T_first_floor_data.append(temp_sensor_first_floor)
    T_second_floor_data.append(temp_sensor_second_floor)
    T_ground_floor_data.append(temp_sensor_ground_floor)
    T_outside_data.append(temp_outside)

    line_first_floor.set_data(time_data, T_first_floor_data)
    line_second_floor.set_data(time_data, T_second_floor_data)
    line_ground_floor.set_data(time_data, T_ground_floor_data)
    line_outside.set_data(time_data, T_outside_data)

    pyplot.plot(time_data, T_first_floor_data, color='blue')
    pyplot.plot(time_data, T_second_floor_data, color='black')
    pyplot.plot(time_data, T_ground_floor_data, color='red')
    pyplot.plot(time_data, T_outside_data, color='orange')
    figure.gca().relim()
    figure.gca().autoscale_view()

    pyplot.legend(['first floor {T: .1f} deg C'.format(T=temp_sensor_first_floor),
                   'second floor {T: .1f} deg C'.format(T=temp_sensor_second_floor),
                   'ground floor {T: .1f} deg C'.format(T=temp_sensor_ground_floor),
                   'outside {T: .1f} deg C'.format(T=temp_outside)], loc = 'lower right')

    ax.set_xlabel('Date-Time')
    ax.set_ylabel('Temp (deg C)')

    return [line_first_floor, line_second_floor, line_ground_floor, line_outside]


def read_data():
    data = {'DateTime': [], 'T_first_floor': [], 'T_ground_floor': [], 'T_second_floor': [], 'T_outside': []}
    df = pd.DataFrame(data)
    hue_data_file = Path(DATA_FILE)
    if not hue_data_file.is_file():  # if the file does not exist; create the file and initialize the data
        df.to_csv(DATA_FILE)
        time_data, T_first_floor_data, T_second_floor_data, T_ground_floor_data, T_outside_data = [], [], [], [], []
    else:  # read historic data from file
        old_df = pd.read_csv(DATA_FILE)
        time_data = pd.to_datetime(old_df['DateTime'], format='%Y-%m-%d %H:%M:%S').to_list()
        T_first_floor_data = old_df['T_first_floor'].to_list()
        T_second_floor_data = old_df['T_second_floor'].to_list()
        T_ground_floor_data = old_df['T_ground_floor'].to_list()
        T_outside_data = old_df['T_outside'].to_list()

    return time_data, T_first_floor_data, T_second_floor_data, T_ground_floor_data, T_outside_data


def initialise_figure():
    figure, ax = pyplot.subplots()
    line_first_floor, = pyplot.plot_date(time_data, T_first_floor_data, '-', color='blue')
    line_second_floor, = pyplot.plot_date(time_data, T_second_floor_data, '-', color='black')
    line_ground_floor, = pyplot.plot_date(time_data, T_ground_floor_data, '-', color='red')
    line_outside, = pyplot.plot_date(time_data, T_outside_data, '-', color='orange')
    return figure, ax, line_first_floor, line_second_floor, line_ground_floor, line_outside


if __name__ == '__main__':
    # read old data file
    (time_data, T_first_floor_data, T_second_floor_data, T_ground_floor_data, T_outside_data) = read_data()

    # TODO prevent loss of connection with bridge
    # setup connection with the hue bridge
    initbridge()
    # getdictionary()
    getsensors("temperature")
    # getlights()

    # inititalize figure for animation
    (figure, ax, line_first_floor, line_second_floor, line_ground_floor, line_outside) = initialise_figure()

    # start the animation  with an interval in ms
    animation = FuncAnimation(figure, update, interval=60000)

    pyplot.show()
