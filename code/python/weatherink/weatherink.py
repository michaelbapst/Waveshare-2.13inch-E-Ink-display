# /*****************************************************************************
# * | File        :	  weatherink.py
# * | Author      :   Michael Bapst (lynxsilver@gmail.com)
# * | Function    :   Retrieves Weather from Open-Meteo and Displays it on a 
# * |             :   Waveshare 2.13in E-Ink Display
# * | Info        :   I wrote this as an exercise to use an E-Ink display, and
# * |             :   get weather info. The GPS function was a bonus.
# * |             :   There are still issues with the code, throws an error when
# * |             :   trying to convert GPS coordinates to a place without name,
# * |             :   etc.
# *----------------
# * | This version:   V1.0
# * | Date        :   1/18/2025
# * | Info        :
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#*****************************************************************************
# The following libraries need to be installed:
# Install Open Meteo: 
# pip install openmeteo-requests
# pip install requests-cache retry-requests numpy pandas
#
# Install geopy
# pip install geopy

import sys
import os
import logging
import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import openmeteo_requests
from convertweather import convertUnixTime, RoundTemp, RoundWindSpeed, HeadingToCompass, DecodeWeatherCode, SecToHours, GetCity
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# For more information about Open-Meteo goto https://open-meteo.com/en/docs
# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
# Change the Lat & Lon to the area you want weather info from. use https://open-meteo.com/en/docs to get your Lat & Lon 
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 64.1355,
	"longitude": -21.8954,
	"current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max"],
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch",
	"timezone": "America/New_York",
	"forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
wAddress = GetCity(response.Latitude(), response.Longitude())

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
wTemp = round(current.Variables(0).Value(), 1)
wHumid =  current.Variables(1).Value()
wWeatherCode, wIcon = DecodeWeatherCode(current.Variables(2).Value())
wWindSpd = round(current.Variables(3).Value(), 2)
wWindDir = HeadingToCompass(current.Variables(4).Value())
wWindGust = round(current.Variables(5).Value(), 2)
wDateTime = convertUnixTime(current.Time())

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
wTempHi = RoundTemp(daily.Variables(1).ValuesAsNumpy())
wTempLo = RoundTemp(daily.Variables(2).ValuesAsNumpy())
wUVIndex = daily.Variables(7).ValuesAsNumpy()

#Setup WaveShare 2.13 V4 
epd = epd2in13_V4.EPD()
epd.init()
#epd.Clear(0xFF)

# Drawing on the image
fontObj = ImageFont.truetype('font.ttc', 10)
wImage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
draw = ImageDraw.Draw(wImage)
draw.text((0, 0), wAddress, font = fontObj, fill = 0)
draw.line([(0,13),(250,13)], fill = 0,width = 1)
draw.text((250, 0), wDateTime, font = fontObj, fill = 0, anchor = "ra")
draw.text((0, 15), "Temp: " + str(wTemp) + " : HI/LO: " + str(wTempHi) + "/" + str(wTempLo), font = fontObj, fill = 0)
draw.text((0, 30), "Humidity: " + str(wHumid), font = fontObj, fill = 0)
draw.text((250, 30), "UVIndex: " + str(wUVIndex), font = fontObj, fill = 0, anchor = "ra")
draw.text((1, 45), "Weather: " + wWeatherCode, font = fontObj, fill = 0)    #Setting the position to 2 keeps the W in weather from getting cut off
draw.text((1, 60), "Wind Speed: " + str(wWindSpd), font = fontObj, fill = 0)
draw.text((1, 75), "Wind Direction: " + str(wWindDir), font = fontObj, fill = 0)
draw.text((1, 90), "Wind Gusts: " + str(wWindGust), font = fontObj, fill = 0)
bmpIcon = Image.open(os.path.join(os.path.dirname(__file__), wIcon))
wImage.paste(bmpIcon,(185,57))
wImage = wImage.rotate(180) # rotate
epd.display(epd.getbuffer(wImage))

# Exit
epd.init()
epd.sleep()
epd2in13_V4.epdconfig.module_exit(cleanup=True)
exit()
