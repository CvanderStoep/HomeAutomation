"""
Python program to find current
weather details of any city
using openweathermap api
"""

# TODO use pyowm library
# wellicht niet meer doen??


# import required modules
import requests  # json
from datetime import datetime, timedelta
from dateutil import tz
import yaml


local = tz.gettz()
print(datetime.now(tz=local))

# Enter your API key here
# api_key = "get api from openweathermap"
from private_info import api_key  # imported from a seperate file, not sychronized to github

# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Give city name
city_name = input("Enter city name : ")

# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name

# get method of requests module
# return response object
response = requests.get(complete_url)

# json method of response object
# convert json format data into
# python format data
x = response.json()
print(x)
sunset_time = x["sys"]["sunset"]
print("sunset, utc time stamp: ", sunset_time)  # timestamp

# TODO automatic correction for Local Time Zone
# local_sunset_time = datetime.utcfromtimestamp(sunset_time) + timedelta(hours=1)  # correct for local timezone
print("current local time: ", datetime.now())  # correct for local timezone
# print("current local sunset: ", local_sunset_time)

# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
print('sunset corrected for TZ: ', datetime.fromtimestamp(sunset_time, tz=local))

print (x.keys())
print(yaml.dump(x))

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if x["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y = x["main"]

    # store the value corresponding
    # to the "temp" key of y
    current_temperature = round(y["temp"] - 273.15, 2)  # convert K to deg C

    # store the value corresponding
    # to the "pressure" key of y
    current_pressure = y["pressure"]

    # store the value corresponding
    # to the "humidity" key of y
    current_humidiy = y["humidity"]

    # store the value of "weather"
    # key in variable z
    z = x["weather"]

    # store the value corresponding
    # to the "description" key at
    # the 0th index of z
    weather_description = z[0]["description"]

    # print following values
    print(" Temperature (in deg Celsius) = " +
          str(current_temperature) +
          "\n atmospheric pressure (in hPa unit) = " +
          str(current_pressure) +
          "\n humidity (in percentage) = " +
          str(current_humidiy) +
          "\n description = " +
          str(weather_description))

else:
    print(" City Not Found ")
