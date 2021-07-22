def hue_lights(bridge):
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

    return data_point

