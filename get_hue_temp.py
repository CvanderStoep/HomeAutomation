def hue_temp(bridge):

    sensors = bridge.get_sensor_objects('id')
    temp_sensor_first_floor = sensors[75].state['temperature'] / 100  # temp in degC
    temp_sensor_ground_floor = sensors[17].state['temperature'] / 100
    temp_sensor_second_floor = sensors[8].state['temperature'] / 100

    print()
    print('Temperature Sensor[8] - second_floor: ', temp_sensor_second_floor)
    print('Temperature Sensor[17] - ground_floor: ', temp_sensor_ground_floor)
    print('Temperature Sensor[75] - first_floor: ', temp_sensor_first_floor)

    data_point = [{'measurement': 'hue_temperature',
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

    return data_point
