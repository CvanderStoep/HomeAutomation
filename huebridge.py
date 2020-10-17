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


def initbridge():
    global bridge
    bridge = Bridge('192.168.68.127')  # connected to Deco mesh
    # bridge.connect() #this command is needed only once; press hue bridge button en run bridge.connect() command.
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
    temp_sensor_zolder = sensors[8].state['temperature'] / 100
    temp_sensor_toilet = sensors[17].state['temperature'] / 100
    temp_sensor_gang = sensors[75].state['temperature'] / 100  # temp in degC

    print()
    print('Temperature Sensor[8] - Zolder 2e etage: ', temp_sensor_zolder)
    print('Temperature Sensor[17] - Toilet BG: ', temp_sensor_toilet)
    print('Temperature Sensor[75] - Gang 1e etage: ', temp_sensor_gang)
    return


def update(frame):
    #activate the sensors and get the data
    sensors = bridge.get_sensor_objects('id')
    temp_sensor_gang = sensors[75].state['temperature'] / 100  # temp in degC
    temp_sensor_toilet = sensors[17].state['temperature'] / 100
    temp_sensor_zolder = sensors[8].state['temperature'] / 100

    #add new time and sensor temperature data to a .csv file
    new_data = {'DateTime': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                'T_gang': [temp_sensor_gang],
                'T_toilet': [temp_sensor_toilet],
                'T_zolder': [temp_sensor_zolder]}
    newdf = pd.DataFrame(new_data)  # only the latest data
    newdf.to_csv('hue_data.csv', mode='a', header=False)
    print('T-zolder last update: ', sensors[8].state['lastupdated'])

    time_data.append(datetime.now())
    T_gang_data.append(temp_sensor_gang)
    T_zolder_data.append(temp_sensor_zolder)
    T_toilet_data.append(temp_sensor_toilet)
    line1.set_data(time_data, T_gang_data)
    line2.set_data(time_data, T_zolder_data)
    line3.set_data(time_data, T_toilet_data)
    pyplot.plot(time_data, T_gang_data, color='blue')
    pyplot.plot(time_data, T_zolder_data, color='black')
    pyplot.plot(time_data, T_toilet_data, color='red')
    figure.gca().relim()
    figure.gca().autoscale_view()
    return [line1, line2, line3]


# below the main program loop starts


if __name__ == '__main__':
    data = {'DateTime': [], 'T_gang': [], 'T_toilet': [], 'T_zolder': []}
    df = pd.DataFrame(data)
    # exportfilename = Path('C:/Users/carlo/OneDrive/Documenten/16. Python/HomeAutomation/hue_data.csv')
    hue_data_file = Path('hue_data.csv')
    if not hue_data_file.is_file(): #if the file does not exist; create the file and initialize the data
        df.to_csv('hue_data.csv')
        time_data, T_gang_data, T_zolder_data, T_toilet_data = [], [], [], []
    else: #read historic data from file
        old_df = pd.read_csv('hue_data.csv')
        time_data = pd.to_datetime(old_df['DateTime'], format='%Y-%m-%d %H:%M:%S').to_list()
        T_gang_data = old_df['T_gang'].to_list()
        T_zolder_data = old_df['T_zolder'].to_list()
        T_toilet_data = old_df['T_toilet'].to_list()

    #TODO prevent loss of connection with bridge
    initbridge()
    # getdictionary()
    # getsensors("temperature")
    # getlights()

    figure, ax = pyplot.subplots()
    line1, = pyplot.plot_date(time_data, T_gang_data, '-', color='blue')
    line2, = pyplot.plot_date(time_data, T_zolder_data, '-', color='black')
    line3, = pyplot.plot_date(time_data, T_toilet_data, '-', color='red')
    ax.set_xlabel('Date-Time')
    ax.set_ylabel('Temp (deg C)')
    pyplot.legend(['gang', 'zolder', 'toilet'])

    #start the animation  with an interval in ms
    animation = FuncAnimation(figure, update, interval=60000)

    pyplot.show()

