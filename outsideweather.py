import requests


def getoutsideweather(city="Delft"):
    # from private_info import complete_url  # combines api key and city for the temperature
    from private_info import web_url
    complete_url = web_url + city
    response = requests.get(complete_url)
    x = response.json()
    y = x["main"]
    wind_speed = x["wind"]["speed"]
    wind_direction = x["wind"]["deg"]
    current_temperature = round(y["temp"] - 273.15, 2)  # convert K to deg C
    weather_type = x["weather"][0]["main"]
    humidity = x["main"]["humidity"]
    pressure = x["main"]["pressure"]
    return current_temperature, wind_speed, weather_type, humidity, pressure, wind_direction
