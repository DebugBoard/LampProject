
# WEATHER DISPLAY - Bartosz Jaskulski
#
#
# --- PLEASE READ ---
# This script is for Pimoroni Inky *wHAT* Displays ONLY
# Please use impression-main.py if you have an Inky Impression
# --- PLEASE READ ---
#
#

import os, sys, time
from datetime import datetime, timedelta
import cond_icons

import configparser

#config.ini file
configObj = configparser.ConfigParser()
configObj.read(os.path.dirname(os.path.realpath(__file__)) + "/configfile.ini")
OWMAPI = configObj["OWM_API"]
UserLoc = configObj["Location"]

api = OWMAPI["api"]

lat =float(UserLoc["latitude"])
lon = float(UserLoc["longitude"])
city = str(UserLoc["city"])
country = str(UserLoc["country"])

#Inky Libraries
from inky import InkyWHAT
from gpiod.line import Value
from PIL import Image, ImageFont, ImageDraw

# pyOWM Libraries
from pyowm.owm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

CURR_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"
RESOURCES = CURR_DIR + "resources/"

# Fonts
PIXEL_FONT = RESOURCES + "fonts/Pixel12x10.ttf"
Terminal_FONT = RESOURCES + "fonts/terminal-grotesque.ttf"
Mister_Pixel_FONT = RESOURCES + "fonts/Mister_Pixel_Regular.otf"
B_FONT = RESOURCES + "fonts/04B_03.ttf"
VG5000_FONT = RESOURCES + "fonts/VG5000-Regular.otf"
FT88Reg_FONT = RESOURCES + "fonts/FT88-Regular.otf"
FT88Bold_FONT = RESOURCES + "fonts/FT88-Bold.otf"
 
TimeDate = datetime.now()
TwoHrsTime = (datetime.now()+timedelta(hours=2)).strftime("%H:00")
FourHrsTime = (datetime.now()+timedelta(hours=4)).strftime("%H:00")
SixHrsTime = (datetime.now()+timedelta(hours=6)).strftime("%H:00")
EightHrsTime = (datetime.now()+timedelta(hours=8)).strftime("%H:00")

degreeSign = u"\N{DEGREE SIGN}"

#OpenWeatherMap Integration
owm = OWM(api)
mgr = owm.weather_manager()
weather = mgr.weather_at_place(city+","+country).weather
one_call = mgr.one_call(lat, lon)

getTemp = weather.temperature("celsius") #enables temp in celsius
curTemp = int(getTemp["temp"]) #get current temp

#Current "feels like" Temperature
feelsLike = int(getTemp["feels_like"])
currentFeelsLike = "Feels: "+str(feelsLike)+degreeSign

#current max and min temps
maxTemp = int(getTemp["temp_max"])
minTemp = int(getTemp["temp_min"])

#Current wind speeds
getWind = weather.wind(unit="miles_hour")
curWind = int(getWind["speed"])

inky_display = InkyWHAT("yellow")
inky_display.set_border(inky_display.WHITE)

Location_ICON = RESOURCES + "icons/location.png"
LocationIcon = Image.open(Location_ICON)

bg = Image.open(RESOURCES + "background/weather-report-bg.png")
img = bg.copy()
img.paste(bg.crop((0, 20, 400, 300)), (0, 0))	#move content up by the 20px header bar
img.paste(bg.crop((0, 0, 400, 20)), (0, 280))	#header bar at the bottom
draw = ImageDraw.Draw(img)

font_tiny = ImageFont.truetype(FT88Bold_FONT, 12)
font_small = ImageFont.truetype(FT88Bold_FONT, 12)
font_medium = ImageFont.truetype(VG5000_FONT, 32)
font_medium2 = ImageFont.truetype(FT88Bold_FONT, 18)
font_big = ImageFont.truetype(VG5000_FONT, 70)
font2 = ImageFont.truetype(VG5000_FONT, 10)

currentTemp = str(curTemp)+degreeSign

currentMaxTemp = "Max: "+str(maxTemp)+degreeSign #current temp max
currentMinTemp = "Min: "+str(minTemp)+degreeSign #current temp min

TwoHrTemp = str(int(one_call.forecast_hourly[2].temperature("celsius").get("temp", 0))) #get temp in 2 hrs
TwoHrCond = str(one_call.forecast_hourly[2].status)
FourHrTemp = str(int(one_call.forecast_hourly[4].temperature("celsius").get("temp", 0))) #get temp in 4 hrs
FourHrCond = str(one_call.forecast_hourly[4].status)
SixHrTemp = str(int(one_call.forecast_hourly[6].temperature("celsius").get("temp", 0))) #get temp in 6 hrs
SixHrCond = str(one_call.forecast_hourly[6].status)
EightHrTemp = str(int(one_call.forecast_hourly[8].temperature("celsius").get("temp", 0))) #get temp in 8 hrs
EightHrCond = str(one_call.forecast_hourly[8].status)

currentCond = str(weather.status)
currentDetailCond = str(weather.detailed_status).title()

currentHumidity = "Hum:"+str(one_call.current.humidity)+"%"
currentWind = "Wind:"+str(curWind)+" MPH"
currentLoc = ": " + city

#proper text placement
projectName = "WEATHER REPORT"
w_name, h_name = font2.getbbox(projectName)[2:]
x_name = 200 - (w_name/2)

w_TwoHrTemp, h_TwoHrTemp = font_medium.getbbox(TwoHrTemp)[2:]
x_TwoHrTemp = (50) - (w_TwoHrTemp/2)
w_TwoHrsTime, h_TwoHrsTime = font_tiny.getbbox(TwoHrsTime)[2:]
x_TwoHrsTime = 50 - (w_TwoHrsTime/2)
w_TwoHrCond, h_TwoHrCond = font_tiny.getbbox(TwoHrCond)[2:]
x_TwoHrCond = 50 - (w_TwoHrCond/2)

w_FourHrTemp, h_FourHrTemp = font_medium.getbbox(FourHrTemp)[2:]
x_FourHrTemp = (150) - (w_FourHrTemp/2)
w_FourHrsTime, h_FourHrsTime = font_tiny.getbbox(FourHrsTime)[2:]
x_FourHrsTime = 150 - (w_FourHrsTime/2)
w_FourHrCond, h_FourHrCond = font_tiny.getbbox(FourHrCond)[2:]
x_FourHrCond = 150 - (w_FourHrCond/2)

w_SixHrTemp, h_SixHrTemp = font_medium.getbbox(SixHrTemp)[2:]
x_SixHrTemp = (250) - (w_SixHrTemp/2)
w_SixHrsTime, h_SixHrsTime = font_tiny.getbbox(SixHrsTime)[2:]
x_SixHrsTime = 250 - (w_SixHrsTime/2)
w_SixHrCond, h_SixHrCond = font_tiny.getbbox(SixHrCond)[2:]
x_SixHrCond = 250 - (w_SixHrCond/2)

w_EightHrTemp, h_EightHrTemp = font_medium.getbbox(EightHrTemp)[2:]
x_EightHrTemp = (350) - (w_EightHrTemp/2)
w_EightHrsTime, h_EightHrsTime = font_tiny.getbbox(EightHrsTime)[2:]
x_EightHrsTime = 350 - (w_EightHrsTime/2)
w_EightHrCond, h_EightHrCond = font_tiny.getbbox(EightHrCond)[2:]
x_EightHrCond = 350 - (w_EightHrCond/2)

#draw data and text onto display

draw.text((5, 284),TimeDate.strftime("%m-%d-%Y"), inky_display.WHITE, font2)	#Time
draw.text((368, 284),TimeDate.strftime("%H:%M"), inky_display.WHITE, font2)	#Date
draw.text((x_name, 284),projectName, inky_display.WHITE, font2)			#project name

draw.text((155, 45), currentTemp, inky_display.BLACK, font_big)				#Current temp
draw.text((292, 80), currentMaxTemp, inky_display.BLACK, font_small)			#Current max temp
draw.text((292, 96), currentMinTemp, inky_display.BLACK, font_small)			#Current min temp
draw.text((292, 50), currentFeelsLike, inky_display.BLACK, font_small)

#img.paste(LocationIcon, (15, 198)) 
#draw.text((35, 200), currentLoc, inky_display.BLACK, font_medium2)			#Current location

draw.text((x_TwoHrTemp, 226), TwoHrTemp+degreeSign, inky_display.BLACK, font_medium)	#Temp in 2 hrs
draw.text((x_FourHrTemp, 226),FourHrTemp+degreeSign, inky_display.BLACK, font_medium)	#Temp in 4 hrs
draw.text((x_SixHrTemp, 226), SixHrTemp+degreeSign, inky_display.BLACK, font_medium)	#Temp in 6 hrs
draw.text((x_EightHrTemp, 226), EightHrTemp+degreeSign, inky_display.BLACK, font_medium)	#Temp in 8 hrs

draw.text((x_TwoHrCond, 263), TwoHrCond, inky_display.BLACK, font_tiny)			#Condition in 2 hrs
draw.text((x_FourHrCond, 263), FourHrCond, inky_display.BLACK, font_tiny)		#Condition in 4 hrs
draw.text((x_SixHrCond, 263), SixHrCond, inky_display.BLACK, font_tiny)			#Condition in 6 hrs
draw.text((x_EightHrCond, 263), EightHrCond, inky_display.BLACK, font_tiny)		#Condition in 8 hrs

draw.text((x_TwoHrsTime, 219), TwoHrsTime, inky_display.BLACK, font_tiny)		#Time in 2 hrs
draw.text((x_FourHrsTime, 219), FourHrsTime, inky_display.BLACK, font_tiny)		#Time in 4 hrs
draw.text((x_SixHrsTime, 219), SixHrsTime, inky_display.BLACK, font_tiny)		#Time in 6 hrs
draw.text((x_EightHrsTime, 219), EightHrsTime, inky_display.BLACK, font_tiny)		#Time in 8 hrs

draw.text((292, 130), currentHumidity, inky_display.BLACK, font_small)			#Current humidity in percentage
draw.text((292, 158), currentWind, inky_display.BLACK, font_small)		#Current wind speed in MPH

draw.text((10, 170), currentDetailCond, inky_display.BLACK, font_medium2)		#Current weather conditions, detailed
img.paste(cond_icons.CurrCondIcon(), (15, 40))                                  #Current Weather Icon

inky_display.set_image(img)
inky_display.show(busy_wait=False)
# Poll BUSY directly: the library's edge-based wait can return early on a stale edge,
# and its 30s timeout is shorter than this panel's ~86s refresh
deadline = time.time() + 180
while inky_display._gpio.get_value(inky_display.busy_pin) == Value.ACTIVE and time.time() < deadline:
	time.sleep(0.1)
inky_display._send_command(0x10, 0x01)	# deep sleep, as show() does after a successful wait
