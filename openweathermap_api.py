import sys
from datetime import datetime
import requests
import re
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
#----------------------------------------------------------------------------

class OpenWeatherMap:
    def __init__(self):
        privatekey = i.OWMapKey()
        self.__key = privatekey.getkey()

    def getkey(self):
        return self.__key

    def chooselocation(self): #from getlocation module
        from getlocation import latitude,longitude,city,cityinfo
        self._city = city
        self._cityinfo = cityinfo
        self._lat = latitude
        self._long = longitude

    def defaultlocation(self): #manually swap between Tampa and Wichita. Skips getlocation process
        Wichita = (-97.3375,37.6922,"Wichita")
        Tampa = (-82.4584,27.9477,"Tampa")
        self._long, self._lat = Tampa[0], Tampa[1]
        self._city = Tampa[2]

    def OWMap_getrequest(self):
        self._url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self._lat}&lon={self._long}&exclude=daily,minutely,alerts&units=imperial&appid={self.getkey()}"
        req = requests.get(self._url)
        if req.status_code == 200:
            self._doc = req.json() #not using BeautifulSoup4 due to the formatting of the API results
        else:
            print(f"An error occurred when sending a get request to OpenWeatherMap's api. Error code: {req.status_code}")
            quit()

    def getspecifiedinfo(self,info):
        '''Dictionary converts inputted terms to accessible terms in the API results. The "with open..."
            portion writes next 48 hours of data to a savefile in a predetermined save location.'''
        apiterms = {
            "temp" : "temp",
            "feels like" : "feels_like",
            "humidity": "humidity",
            "precip" : "pop",
            "clouds" : "clouds",
            "visibility" : "visibility",
            "wind speed" : "wind_speed",
            "wind dir" : "wind_deg",
            "wind gust" : "wind_gust",
            "uv index" : "uvi"
        }

        with open(f'{directory}/Weather_API_webscraper/save files/openweathermap req savefiles/{self._city} {datetime.now().strftime("%Y-%m-%d %H.%M")}.txt',"w") as file:
            file.write(f"City: {self._city}")# in {cityinfo}\n\n")
            file.write(f"\nCurrent time: {datetime.now()}\n\n")

            #hourly data
            file.write("Hourly Data:\n" + "-"*40 + "\n")
            file.write("Temperature in Farenheit (F)\nWind Speed in miles per hour (mph)\n" + "-"*40 + "\n")

            for n in range(0,48): #range function excludes terminating value. captures hours 0-47
                file.write(f"unix time:{self._doc['hourly'][n]['dt']}\n")
                file.write(f"datetime:{datetime.fromtimestamp(self._doc['hourly'][n]['dt'])}\n")
                for item in info:
                    file.write(f"{item}:{self._doc['hourly'][n][apiterms[item]]}\n")
                file.write("\n")


    def gettodaysindex(self):
        self.current_hour = datetime.fromtimestamp(self._doc['current']['dt']).strftime("%H") #only returns the hour value
        self.remaining_hours_in_the_day = 24 - int(self.current_hour) #length/last index for remaining today's hours


    def gettomorrowshoursindex(self):
        global lower_index_of_tomorrow_hours,upper_index_of_tomorrow_hours
        lower_index_of_tomorrow_hours = self.remaining_hours_in_the_day+1
        upper_index_of_tomorrow_hours = self.remaining_hours_in_the_day+23


#functions to get different pieces of data. Each have their own ranges of times throughout the day, hence separate functions
    def gettemperature(self): #current hour to 7pm (19:00)
        self.temperature = max(self._doc['hourly'][i]['temp'] for i in range(0,lower_index_of_tomorrow_hours-4)) 

        #finding index & hour of max temp
        temp = 0
        self.index_of_temperature = 0
        for i in range(0,lower_index_of_tomorrow_hours-4):
            temp = self._doc['hourly'][i]['temp']
            if temp == self.temperature:
                break
            self.index_of_temperature += 1
        self.hour_of_temperature = datetime.fromtimestamp(self._doc['hourly'][self.index_of_temperature]['dt'])


    def getfeels_like(self): #current hour to 7pm (19:00)
        self.feels_like = max(self._doc['hourly'][i]['feels_like'] for i in range(0,lower_index_of_tomorrow_hours-4)) 

        #finding index & hour of max feels like temp
        feels = 0
        self.index_of_feels_like = 0
        for i in range(0,lower_index_of_tomorrow_hours-4):
            feels = self._doc['hourly'][i]['feels_like']
            if feels == self.feels_like:
                break
            self.index_of_feels_like += 1
        
        self.hour_of_feels_like = datetime.fromtimestamp(self._doc['hourly'][self.index_of_feels_like]['dt'])


    def gettodaymaxuvindex(self): #all day
        self.max_uvindex_today = max([self._doc['hourly'][i]['uvi'] for i in range(0,lower_index_of_tomorrow_hours)]) #range function excludes 00:00 of next day

        #finding index & hour of max uvindex
        uv = 0
        self.index_of_max_uvindex_today = 0
        for i in range(0,lower_index_of_tomorrow_hours):
            uv = self._doc['hourly'][i]['uvi']
            if uv == self.max_uvindex_today:
                break
            self.index_of_max_uvindex_today += 1

        self.hour_of_max_uvindex_today = datetime.fromtimestamp(self._doc['hourly'][self.index_of_max_uvindex_today]['dt'])


    def getmorning_ws(self): #current hour to 11am (11:00)
        self.morning_ws = max([self._doc['hourly'][i]['wind_speed'] for i in range(0,self.remaining_hours_in_the_day-12)])

        #finding index & hour of morning windspeed
        ws = 0
        self.index_of_morning_ws = 0
        for i in range(0,self.remaining_hours_in_the_day-12):
            ws = self._doc['hourly'][i]['wind_speed']
            if ws == self.morning_ws:
                break
            self.index_of_morning_ws += 1

        self.hour_of_morning_ws = datetime.fromtimestamp(self._doc['hourly'][self.index_of_morning_ws]['dt'])


    def getmiddayws(self): #current hour to 5pm (17:00)
        self.midday_ws = max([self._doc['hourly'][i]['wind_speed'] for i in range(0,self.remaining_hours_in_the_day-6)])

        #finding index & hour of first occurence of midday windspeed
        ws = 0
        self.index_of_midday_ws = 0
        for i in range(0,self.remaining_hours_in_the_day-6):
            ws = self._doc['hourly'][i]['wind_speed']
            if ws == self.midday_ws:
                break
            self.index_of_midday_ws += 1

        self.hour_of_midday_ws = datetime.fromtimestamp(self._doc['hourly'][self.index_of_midday_ws]['dt'])


    def getmaxws(self): #all day
        self.max_ws = max([self._doc['hourly'][i]['wind_speed'] for i in range(0,self.remaining_hours_in_the_day)])

        #finding index & hour of first occurence of max windspeed
        ws = 0
        self.index_of_max_ws = 0
        for i in range(0,self.remaining_hours_in_the_day):
            ws = self._doc['hourly'][i]['wind_speed']
            if ws == self.max_ws:
                break
            self.index_of_max_ws += 1

        self.hour_of_max_ws = datetime.fromtimestamp(self._doc['hourly'][self.index_of_max_ws]['dt'])


    def getwind_gust(self): #current hour to 5pm (17:00)
        self.wind_gust = max([self._doc['hourly'][i]['wind_gust'] for i in range(0,self.remaining_hours_in_the_day-6)])

        #finding index & hour of first occurence of wind gust value
        gust = 0
        self.index_of_wind_gust = 0
        for i in range(0,self.remaining_hours_in_the_day-6):
            gust = self._doc['hourly'][i]['wind_gust']
            if gust == self.wind_gust:
                break
            self.index_of_wind_gust += 1

        self.hour_of_wind_gust = datetime.fromtimestamp(self._doc['hourly'][self.index_of_wind_gust]['dt'])
    
    def get_midday_wind_gust(self): #11am to 5pm. Only excecute if 11am exists in data. otherwise execute regular wind_gust
        self.midday_wgust = max([self._doc['hourly'][i]['wind_gust'] for i in range(self.remaining_hours_in_the_day-12,self.remaining_hours_in_the_day-6)])

        #finding index & hour of first occurence of midday wind gust value
        wgust = 0
        self.index_of_midday_wgust = 0
        for i in range(self.remaining_hours_in_the_day-12,self.remaining_hours_in_the_day-6):
            wgust = self._doc['hourly'][i]['wind_gust']
            if wgust == self.wind_gust:
                break
            self.index_of_midday_wgust += 1

        self.hour_of_midday_wgust = datetime.fromtimestamp(self._doc['hourly'][self.index_of_midday_wgust]['dt'])


    def getprecip(self): #current hour to 5pm
        self.precip = max([self._doc['hourly'][i]['pop'] for i in range(0,self.remaining_hours_in_the_day-6)])

        #finding index & hour of first occurence of precipitation high
        pop = 0
        self.index_of_precip = 0
        for i in range(0,self.remaining_hours_in_the_day-6):
            pop = self._doc['hourly'][i]['pop']
            if pop == self.precip:
                break
            self.index_of_precip += 1

        self.hour_of_precip = datetime.fromtimestamp(self._doc['hourly'][self.index_of_precip]['dt'])


    def BackupResults(self):
        with open(f'{directory}/Weather_API_webscraper/save files/openweathermap req savefiles/{self._city} {datetime.now().strftime("%Y-%m-%d %H.%M")}.txt',"a") as file:

            #Extra data
            file.write("\nAdditional Info:\n" + "-"*40 + "\n")

            file.write(f"Today's High (F): {self.temperature} at {self.hour_of_temperature.strftime('%H:%M')}\n")
            file.write(f"Feels Like: {self.feels_like} at {self.hour_of_feels_like.strftime('%H:%M')}\n")
            file.write(f"Today's Max UVindex: {self.max_uvindex_today} at {self.hour_of_max_uvindex_today.strftime('%H:%M')}\n")
            if self.remaining_hours_in_the_day-12 > 0: #if 11am data exists
                file.write(f"Max morning windspeed (7-11am): {self.morning_ws} at {self.hour_of_morning_ws}\n")
            else:
                file.write("It is already past 11am. No morning windspeed data.\n")

            if self.remaining_hours_in_the_day-6 > 0: #if 5pm data exists
                file.write(f"Mid-day windspeed (11am-5pm): {self.midday_ws} at {self.hour_of_midday_ws.strftime('%H:%M')}\n")
            else:
                file.write(f"current hour past 5pm: {self.current_hour}. No mid-day windspeed data.\n")

            file.write(f"Today's Max Wind Speed: {self.max_ws} at {self.hour_of_max_ws.strftime('%H:%M')}\n")
            if self.remaining_hours_in_the_day-12 > 0:
                file.write(f"Mid-day, Expect wind gusts of up to {self.midday_wgust} at {self.hour_of_midday_wgust.strftime('%H:%M')}\n")
            else:
                file.write(f"Expect wind gusts of up to {self.wind_gust} at {self.hour_of_wind_gust.strftime('%H:%M')}\n")
            file.write(f"Max wind gust: {self.wind_gust} at {self.hour_of_wind_gust.strftime('%H:%M')}\n")

            if self.precip > 0.75: #75% chance
                file.write(f"High chance of rain today: {self.precip} at {self.hour_of_precip.strftime('%H:%M')}\n")
            else:
                file.write(f"Don't expect rain today: {self.precip}")


            file.write("\n"*3)
            file.write("API Results:\n")
            file.write("-"*80 + "\n")
            file.write(str(self._doc))


    def createmessage(self):
        message= f'''High: {self.temperature}°F\nFeels like: {self.feels_like}°F\nUVindex: {self.max_uvindex_today} @{self.hour_of_max_uvindex_today.strftime('%H:%M')}\n'''

        if self.remaining_hours_in_the_day-6 > 0:
            message += f"Windspeed up to {self.midday_ws}mph @{self.hour_of_midday_ws.strftime('%H:%M')}\n"
            if self.remaining_hours_in_the_day-12 > 0: #11am to 5pm
                message += f"with gusts of {self.midday_wgust}mph @{self.hour_of_midday_wgust.strftime('%H:%M')}\n"
            else: #executes after 5pm
                message += f"with gusts of {self.wind_gust}mph @{self.hour_of_wind_gust.strftime('%H:%M')}\n"
            if self.midday_ws >= 15:
                message+= "Not a good day to wear certain attire.\n"
        
        if self.precip < 0.75:
            message += f"No rain. {self.precip*100}% chance\n"
        if self.precip >= 0.75:
            message += f"might rain today. {self.precip*100}% chance\n"

        return message
