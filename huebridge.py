from phue import Bridge
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime

data = {'DateTime':[], 'T_gang':[], 'T_toilet':[], 'T_zolder':[]}
df = pd.DataFrame(data)
#documentation can be found at below link:
# https://github.com/studioimaginaire/phue

# bridge = Bridge('192.168.2.3') #connected to router
bridge = Bridge('192.168.68.127') #connected to Deco mesh
# bridge.connect() #this command is needed only once; press hue bridge button en run bridge.connect() command.
#returns a full dictionary
huedictionary = bridge.get_api()
print('Output full dictionary of Hue Bridge:')
print('(Individual objects will be listed after this full dictionary)')
for x,y in huedictionary.items():
    print(x,y)
# print(huedictionary['lights']['1']['state']['colormode'])
# print(len(huedictionary))

#get a flat list of light objects
lights = bridge.lights
# print(lights)
print()
print()
print('Output for all lights:')
for light in lights:
    # if light.on:
        print(light.light_id, light.name, light.on, light.brightness, light.type)

#get a flat list of sensor objects
sensors = bridge.sensors
print()
print('Output for all sensors:')

for sensor in sensors:
    print(sensor.sensor_id, sensor.name, sensor.state)

#get a dictionary with sensor id as key
sensors = bridge.get_sensor_objects('id')
temp_sensor_gang1 = sensors[75].state['temperature']/100 #temp in degC
temp_sensor_toilet = sensors[17].state['temperature']/100
temp_sensor_zolder = sensors[8].state['temperature']/100

print()
print('Temperature Gang 1e etage: ', temp_sensor_gang1)
print('Temperature Toilet BG: ', temp_sensor_toilet)
print('Temperature Zolder 2e etage: ', temp_sensor_zolder)

#get a dictionary with lights id as the key
lights = bridge.get_light_objects('id')
# print(len(lights))
# for i in range(1,len(lights)):
#     print(lights[i])

print(bridge.get_light(11, 'on'))
if temp_sensor_zolder > 24:
    bridge.set_light([11], 'on', True)
    bridge.set_light([11], 'bri', 50)
if temp_sensor_zolder > 25:
    bridge.set_light([12], 'on', True)
    bridge.set_light([12], 'bri', 100)

current_status = bridge.get_light(11, 'on')
while True:
    # if current_status != bridge.get_light(11, 'on'):
    #     print ('change in status')
    #     current_status = bridge.get_light(11, 'on')
    #     if current_status:
    #         print('lights turned on')
    #     else:
    #         print('lights turned off')

    sensors = bridge.get_sensor_objects('id')
    temp_sensor_gang1 = sensors[75].state['temperature'] / 100  # temp in degC
    temp_sensor_toilet = sensors[17].state['temperature'] / 100
    temp_sensor_zolder = sensors[8].state['temperature'] / 100


    new_data = {'DateTime':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'T_gang':temp_sensor_gang1,
                    'T_toilet':temp_sensor_toilet,
                    'T_zolder':temp_sensor_zolder}
    df = df.append(new_data, ignore_index=True)
    print(df)
    print('T-zolder last update: ', sensors[8].state['lastupdated'])
    time.sleep(60)




# b.set_light([11, 12], 'on', True)
# b.set_light([11, 12], 'bri', 254)
# # b.set_light(11, 'on', False)
#
# command_aan = {'transitiontime' : 100, 'on' : True, 'bri' : 254}
# command_uit = {'transitiontime' : 100, 'on' : False}
# # b.set_light(12, command_aan)
# b.set_light(12, command_uit)







