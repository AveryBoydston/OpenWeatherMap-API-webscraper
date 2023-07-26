#https://www.weather.gov/documentation/services-web-api <<< page on how to access API info
import requests
import json

#Tampa:  https://api.weather.gov/points/28.0589,-82.4139 
#   USF lat/long: 28.0589,-82.4139, corresponding "grid": X=72 Y=102, "gridID"=TBW
#
#       "forecast": "https://api.weather.gov/gridpoints/TBW/72,102/forecast",
#       "forecastHourly": "https://api.weather.gov/gridpoints/TBW/72,102/forecast/hourly",
#       "observationStations": "https://api.weather.gov/gridpoints/TBW/72,102/stations",

#Wichita: https://api.weather.gov/points/37.7361,-97.2451
#   Five Guys lat/long: 37.7361, -97.2451, corresponding "grid": X=65 Y=36, "gridID"=ICT
#
#        "forecast": "https://api.weather.gov/gridpoints/ICT/65,36/forecast",
#        "forecastHourly": "https://api.weather.gov/gridpoints/ICT/65,36/forecast/hourly",
#        "observationStations": "https://api.weather.gov/gridpoints/ICT/65,36/stations",


def jprint(obj):
    text = json.dumps(obj,sort_keys =
     True,indent = 4)
    print (text)

# parameters = {
#     "": ,
#     "": 
# }

response = requests.get('https://www.weather.com/')#,params=parameters)
print(response.status_code)

jprint(response.json())