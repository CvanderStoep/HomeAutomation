from phue import Bridge

#documentation can be found at below link:
# https://github.com/studioimaginaire/phue

# b = Bridge('192.168.2.3') #connected to router
b = Bridge('192.168.68.127') #connected to Deco mesh
# b.connect() #this command is needed only once; press hue bridge button en run b.connect() command.
#returns a full dictionary
huedictionary = b.get_api()
print('Output full dictionary of Hue Bridge:')
print('(Individual objects will be listed after this full dictionary)')
for x,y in huedictionary.items():
    print(x,y)
# print(huedictionary['lights']['1']['state']['colormode'])
# print(len(huedictionary))

#get a flat list of light objects
lights = b.lights
# print(lights)
print()
print('Output for all lights:')
for light in lights:
    # if light.on:
        print(light.light_id, light.name, light.on, light.brightness, light.type)

#get a flat list of sensor objects
sensors = b.sensors
print()
print('Output for all sensors:')

for sensor in sensors:
    print(sensor.sensor_id, sensor.name, sensor.state)

#get a dictionary with sensor id as key
sensors = b.get_sensor_objects('id')
temp_sensor_gang1 = sensors[75].state['temperature']/100 #temp in degC
temp_sensor_toilet = sensors[17].state['temperature']/100
temp_sensor_zolder = sensors[8].state['temperature']/100

print()
print('Temperature Gang 1e etage: ', temp_sensor_gang1)
print('Temperature Toilet BG: ', temp_sensor_toilet)
print('Temperature Zolder 2e etage: ', temp_sensor_zolder)

#get a dictionary with lights id as the key
lights = b.get_light_objects('id')
# print(len(lights))
# for i in range(1,len(lights)):
#     print(lights[i])

print(b.get_light(11, 'on'))
if temp_sensor_zolder > 24:
    b.set_light([11], 'on', True)
    b.set_light([11], 'bri', 50)
if temp_sensor_zolder > 25:
    b.set_light([12], 'on', True)
    b.set_light([12], 'bri', 100)



# b.set_light([11, 12], 'on', True)
# b.set_light([11, 12], 'bri', 254)
# # b.set_light(11, 'on', False)
#
# command_aan = {'transitiontime' : 100, 'on' : True, 'bri' : 254}
# command_uit = {'transitiontime' : 100, 'on' : False}
# # b.set_light(12, command_aan)
# b.set_light(12, command_uit)







