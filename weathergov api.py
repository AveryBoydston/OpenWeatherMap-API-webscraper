#This api webscraper utilizes the weather.gov api to pull info regarding current and near future
#information on windspeed and time for predetermined locations 


#https://www.weather.gov/documentation/services-web-api <<< page on how to access API info
import requests
import re
from pathlib import Path
import os
import pprint
#from bs4 import BeautifulSoup - not needed because format of page is not organized in HTML format

#Available locations: ----------------------------------------------------------------------------------------------
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

def getlocation():
    location = "wichita".lower() #change to input later

    while location != (("wichita") or ("tampa") or "1"):
        location = input("You may have entered the wrong place. Please enter a valid input or type 1 to stop: ")

    if location == "tampa":
        url = "https://api.weather.gov/gridpoints/TBW/72,102/forecast/hourly"
    if location == "wichita":
        url = "https://api.weather.gov/gridpoints/ICT/65,36/forecast/hourly"
    return url,location
url,location = getlocation()

def request(url):
    req = requests.get(url)
    if req.status_code == 200:
        doc = req.text #not using bs4 because this HTML in particular is not easily navigable. All the info is under a single tag
        return doc
    else:
        print(f"An error occurred when sending a get request to {url}. Error code: {req.status_code}")
doc = request(url)

#creating backup of response results in case of debugging 
def tempsaveHTML(doc):
    with open("weathergov_tempsavefile.txt","w") as file: #saving results in case of error
        file.write(doc)
    #pprint.pprint(json.loads(results.content)) #in case for debuggin
tempsaveHTML(doc)


#-=-=-=-=-=- finding hourly date & time -=-=-=-=-=-
def get_times():
    time_pattern = re.compile(r"[\"]startTime[\"]: [\"]\d{4}-\d{2}-\d{2}T\d{2}:\d{2}") #ignoring the -04:00
    matches = time_pattern.findall(doc) #findall instead of finditer because I want a list

    time_list = [] #adding results into list
    for time in matches:
        time_list.append(time)
    
    
    #removing everything but the date and time
    time_list = [char.replace('"startTime": "','') for char in time_list] 
    time_list = [char.replace('T',' ') for char in time_list]
    
    print (time_list)
#    print(f"{len(time_list)} items\n\n") #number of results must match for each time and data
    return time_list
time_list = get_times()

#finding today's date
def todaysdate():
    date_find = re.compile(r"\d{4}-\d{2}-\d{2}")
    todays_date = date_find.match(time_list[0]).group() #.group extracts date from RegEx format
    return todays_date
today = todaysdate()

#finding the current hour
current_hour = time_list[0].replace(f'{today} ','')



time_dict = {
    '01:00' : '1am',
    '02:00' : '2am',
    '03:00' : '3am',
    '04:00' : '4am',
    '05:00' : '5am',
    '06:00' : '6am',
    '07:00' : '6am',
    '08:00' : '8am',
    '09:00' : '9am',
    '10:00' : '10am',
    '11:00' : '11am',
    '12:00' : '12pm',
    '13:00' : '1pm',
    '14:00' : '2pm',
    '15:00' : '3pm',
    '16:00' : '4pm',
    '17:00' : '5pm',
    '18:00' : '6pm',
    '19:00' : '7pm',
    '20:00' : '8pm',
    '21:00' : '9pm',
    '22:00' : '10pm',
    '23:00' : '11pm',
}


#relocating save file
def relocate(location,today):
    source_file = Path("C:/Users/avboy/Documents/GitHub - Personal/weathergov_tempsavefile.txt") #will mess up if changing computers with different names
    destination_file = Path(f"C:/Users/avboy/Documents/GitHub - Personal/Weather-API-webscraper/save files/weathergov req savefiles/{location} {today}.txt")
#                    ^^^^^ needs to be changed based on device pathing
    #if file aready exists, alter name
    n=1
    while os.path.isfile(destination_file) is True:
        destination_file = Path(f"C:/Users/avboy/Documents/GitHub - Personal/Weather-API-webscraper/save files/weathergov req savefiles/{location} {today}({n}).txt")
        n+=1



    source_file.rename(destination_file)

relocate(location,today)

#-=-=-=-=-=- hourly windspeed -=-=-=-=-=-
def get_windspeed(doc):
    windspeed_pattern = re.compile(r"\d\d* mph")

    matches = windspeed_pattern.findall(doc) #findall instead of finditer because i want a list

    all_windspeeds = []
    for match in matches:
        all_windspeeds.append(match)

#    print(all_windspeeds)
#    print(f"{len(all_windspeeds)} items\n\n")
    return all_windspeeds
all_windspeeds = get_windspeed(doc)



#obtaining a list of windspeed integer values
windspeed_ints = all_windspeeds #copying list
windspeed_ints = [char.replace(' mph','') for char in windspeed_ints] #removing nondigit substring
windspeed_ints = list(map(int, windspeed_ints)) #converts item to int
print(windspeed_ints)



#separate list for just today's windspeeds integers
todays_windspeed_ints = windspeed_ints[time_list.index(f'{today} {current_hour}'):time_list.index(f'{today} 23:00')]
print(todays_windspeed_ints)



#-=-=-=-=-=- finding today's morning, mid-day, and max all_windspeeds -=-=-=-=-=-

#--- morning windspeed via time---
#8am
if f'{today} 8:00' in time_list:
    eight_am_index = time_list.index(f'{today} 8:00')
    print(f"Today's 8am windspeed will be {all_windspeeds[eight_am_index]}.")

#or most recent time
else: #if at a later time than 8am
    current_hour_index = time_list.index(f'{today} {current_hour}')

    print(f"current wind speed: {all_windspeeds[current_hour_index]} at {time_dict[current_hour]}")


#--- mid-day all_windspeeds (10am-3pm) ---
if f'{today} 15:00' in time_list:
    #10am earliest time
    if f'{today} 10:00' in time_list: 
        am_index = time_list.index(f'{today} 10:00')
    else:
        am_index = time_list.index(f'{today} {current_hour}')

    three_pm_index = time_list.index(f'{today} 15:00')

    max_mid_day_windspeed = max(windspeed_ints[am_index:three_pm_index])
    print(f"The max windspeed around lunchtime will be {max_mid_day_windspeed}mph today.")
else:
    pass
#--- first instance of today's max windspeed and the associated time ---
max_speed = max(todays_windspeed_ints)
max_speed_index = todays_windspeed_ints.index(max_speed)
#print(f"max speed: {max_speed}")
#print(f"max speed index - {max_speed_index}")

#
time_of_max_speed = time_list[max_speed_index]
#print(f"time of max speed: {time_of_max_speed}")
# print(time_list.index(time_of_max_speed))


def max_hour():
    max_hour_find = re.compile(r"\d{2}:\d{2}")
    hour = max_hour_find.search(time_of_max_speed).group() #.group extracts hour from RegEx format
    
    return hour
todays_max_hour = max_hour()

print(f"Today's max speed will be {max_speed}mph at {time_dict[todays_max_hour]}.")



#-=-=-=-=-=- tomorrow's max speed throughout the day -=-=-=-=-=-


