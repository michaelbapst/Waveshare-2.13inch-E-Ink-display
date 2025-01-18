# /*****************************************************************************
# * | File        :	  convertweather.py
# * | Author      :   Michael Bapst (lynxsilver@gmail.com)
# * | Function    :   Various conversion functions used by Weather Ink python app
# * | Info        :
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
#
# Install geopy : pip install geopy
#
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from datetime import datetime
import numpy as np

def GetCity(Lat, Lon):
	geolocator = Nominatim(user_agent="E-Ink_Weather_App")
	try:
		location = geolocator.reverse(str(Lat) + "," + str(Lon))
		address = location.raw['address']

		# Traverse the data
		city = address.get('city', '')
		state = address.get('state', '')
		code = address.get('country_code')
		addrss = city + ", " + state + ", " + code.upper()
		return addrss
	except GeocoderServiceError as e:
		print("Error: ", e)
		return "ERROR"

def convertUnixTime(UnixTime):
	# Convert UNIX time to Modern
	return datetime.utcfromtimestamp(UnixTime).strftime('%a, %b %-d, %Y %-I:%-M:%-S %p')

def RoundTemp(Temperature):
	# Cleanup temperature
	return np.round(Temperature, 1)

def RoundWindSpeed(WindSpeed):
        # Cleanup Wind Speed
        return np.round(WindSpeed, 2)

def HeadingToCompass(Heading):
        # Convert Heading to Compass points (N-NE-E-SE-S-SW-W-NW)
	# Converts a heading in degrees to a compass direction.

	directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
	          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
	index = round(Heading / 22.5) % 16
	return directions[index]

def DecodeWeatherCode(WeatherCode):
    match WeatherCode:
        case 0:
            return "Clear Sky", "icon/wmo_icon_00d.bmp"
        case 1:
            return "Mainly Clear", "icon/wmo_icon_01d.bmp"
        case 2:
            return "Partly Cloudy", "icon/wmo_icon_02d.bmp"
        case 3:
            return "Overcast", "icon/wmo_icon_03d.bmp"
        case 45:
            return "Fog", "icon/wmo_icon_45d.bmp"
        case 48:
            return "Freezing Fog", "icon/wmo_icon_45d.bmp"
        case 51:
            return "Light Drizzle", "icon/wmo_icon_53d.bmp"
        case 53:
            return "Moderate Drizzle", "icon/wmo_icon_53d.bmp"
        case 55:
            return "Heavy Drizzle", "icon/wmo_icon_53d.bmp"
        case 56:
            return "Light Freezing Drizzle", "icon/wmo_icon_57d.bmp"
        case 57:
            return "Heavy Freezing Drizzle", "icon/wmo_icon_57d.bmp"
        case 61:
            return "Light Rain", "icon/wmo_icon_61d.bmp"
        case 63:
            return "Moderate Rain", "icon/wmo_icon_61d.bmp"
        case 65:
            return "Heavy Rain", "icon/wmo_icon_65d.bmp"
        case 66:
            return "Light Freezing Rain", "icon/wmo_icon_66d.bmp"
        case 67:
            return "Heavy Freezing Rain", "icon/wmo_icon_67d.bmp"
        case 71:
            return "Light Snow", "icon/wmo_icon_71d.bmp"
        case 73:
            return "Moderate Snow", "icon/wmo_icon_73d.bmp"
        case 75:
            return "Heavy Snow", "icon/wmo_icon_75d.bmp"
        case 77:
            return "Snow Pellets", "icon/wmo_icon_75d.bmp"
        case 80:
            return "Light Rain Showers", "icon/wmo_icon_80d.bmp"
        case 81:
            return "Moderate Rain Showers", "icon/wmo_icon_81d.bmp"
        case 82:
            return "Heavy Rain Showers", "icon/wmo_icon_81d.bmp"
        case 85:
            return "Light Snow Showers", "icon/wmo_icon_85d.bmp"
        case 86:
            return "Heavy Snow Showers", "icon/wmo_icon_86d.bmp"
        case 95:
            return "Thunderstorms", "icon/wmo_icon_95d.bmp"
        case 96:
            return "Thunderstorms with Light Hail", "icon/wmo_icon_96d.bmp"
        case 99:
            return "Thunderstorms with Heavy Hail", "icon/wmo_icon_96d.bmp"
        case _:
            return "Invalid Weather Code", "icon/wmo_icon_err.bmp"

def SecToHours(seconds):
	numHr = np.round(int(seconds/3600), 0)
	numMin = np.round(int((seconds%3600)/60), 0)
	numSec = np.round(int((seconds%3600)%60), 0)
	#strHr = ["{:0f} hrs {:0f} mins {:0f} secs".format(float(numHr), float(numMin), float(numSec))]
	strHr = ["{} hrs {} mins {} secs".format(numHr, numMin, numSec)]
	return strHr
