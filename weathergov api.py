#https://www.weather.gov/documentation/services-web-api <<< page on how to access API info
import requests
import re
from pathlib import Path
import pprint
#from bs4 import BeautifulSoup - not needed because format of page is not organized in HTML format

#----------------------------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------
#variable location choosing
location = "Wichita" #change to input later

if location == "Wichita":
    url = "https://api.weather.gov/gridpoints/TBW/72,102/forecast/hourly"
if location == "Tampa":
    url = "https://api.weather.gov/gridpoints/ICT/65,36/forecast/hourly"


results = requests.get(url)
if results.status_code == 200:
    pass
else:
    print(f"An error occurred when sending a get request to {url}. Error code {results.status_code}")
doc = results.text #not using bs4 because this HTML in particular is not easily navigable. All the info is under a single tag



#creating backup of response results in case of debugging 
with open("results_tempsavefile.txt","w") as file: #saving results in case of error
    file.write(doc)
#pprint.pprint(json.loads(results.content)) #in case for debuggin



#-=-=-=-=-=- finding hourly date & time -=-=-=-=-=-
time_pattern = re.compile(r"[\"]startTime[\"]: [\"]\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}") #ignoring the -04:00
matches = time_pattern.findall(doc) #findall instead of finditer because I want a list

time_list = [] #adding results into list
for time in matches:
    time_list.append(time)

#removing everything but the date and time
time_list = [time.replace('"startTime": "','') for time in time_list] 
time_list = [time.replace('T',' ') for time in time_list]
print (time_list)

print(f"{len(time_list)} items\n\n") #number of results must match for each time and data



#finding today's date to add to the the results save file
date_find = re.compile(r"\d{4}-\d{2}-\d{2}")
todays_date = date_find.match(time_list[0])
todays_date=todays_date.group()

source_file = Path("C:/Users/avboy/Documents/GitHub - Personal/results_tempsavefile.txt") #will mess up if changing computers with different names
destination_file = Path(f"C:/Users/avboy/Documents/GitHub - Personal/Weather-API-webscraper/weathergov request savefiles/{location} {todays_date}.txt")
#                    ^^^^^ needs to be changed based on device pathing

source_file.rename(destination_file)

#-=-=-=-=-=- hourly windspeed -=-=-=-=-=-
windspeed_pattern = re.compile(r"\d\d* mph")

matches = windspeed_pattern.findall(doc) #findall instead of finditer because i want a list

windspeed_list = []
for match in matches:
    windspeed_list.append(match)
print(windspeed_list)
print(f"{len(windspeed_list)} items\n\n")




