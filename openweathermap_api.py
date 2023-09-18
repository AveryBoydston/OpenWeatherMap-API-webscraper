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

    def defaultlocation(self):
        Wichita = (-97.3375,37.6922,"Wichita")
        Tampa = (-82.4584,27.9477,"Tampa")
        self._long = Wichita[0]
        self._lat = Wichita[1]
        self._city = Wichita[2]

    def OWMap_getrequest(self):
        self._url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self._lat}&lon={self._long}&exclude=daily,minutely,alerts&units=imperial&appid={self.getkey()}"
        req = requests.get(self._url)
        if req.status_code == 200:
            self._doc = req.json() #not using BeautifulSoup due to the formatting of the API results
            return self._doc
        else:
            print(f"An error occurred when sending a get request to OpenWeatherMap's api. Error code:{req.status_code}")
            quit()


    def getspecifiedinfo(self,info):        
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

        self.data = {}

        with open(f'{directory}/Weather-API-webscraper/save files/openweathermap req savefiles/{self._city} {datetime.now().strftime("%Y-%m-%d %H.%M")}.txt',"w") as file:
            file.write(f"City: {self._city}\n\n")# in {cityinfo}\n\n")

            #hourly data
            file.write("Hourly:\n" + "-"*40 + "\n")

            for n in range(0,48): #range function excludes terminating value, in this case 48
                file.write(f"unix time:{self._doc['hourly'][n]['dt']}\n")
                file.write(f"datetime:{datetime.fromtimestamp(self._doc['hourly'][n]['dt'])}\n")
                for item in info:
                    file.write(f"{item}:{self._doc['hourly'][n][apiterms[item]]}\n")
                file.write("\n")


    def gettodaysindex(self):
        global current_hour,remaining_hours_in_the_day
        current_hour = datetime.fromtimestamp(self._doc['current']['dt']).strftime("%H") #only returns the hour value
        remaining_hours_in_the_day = 24 - int(current_hour) #length/last index for remaining today's hours

    def gettomorrowshoursindex(self):
        global lower_index_of_tomorrow_hours,upper_index_of_tomorrow_hours
        lower_index_of_tomorrow_hours = remaining_hours_in_the_day+1
        upper_index_of_tomorrow_hours = remaining_hours_in_the_day+23
        print(f"last hour of tmrw: {datetime.fromtimestamp(self._doc['hourly'][upper_index_of_tomorrow_hours]['dt'])}")
        print(upper_index_of_tomorrow_hours)


    def gettodaymaxuvindex(self):
        self.max_uvindex_today = max([self._doc['hourly'][i]['uvi'] for i in range(0,remaining_hours_in_the_day+1)])
        
        #finding hour of max uvindex:
        for n in range(0,remaining_hours_in_the_day+1):
            
        pattern = re.compile(r'"uvi":[\.\d]')
        matches = pattern.finditer(str(self._doc))
        for match in matches:
            print(match.group())
#        self.hour_of_max_uvindex_today = self._doc['hourly'][i]['uvi']

        
        # self.max_uvindex_today = max(self.todaydata["uvindex"])
        # self.hour_of_max_uvindex_today = self.todaydata["time"][(self.todaydata["uvindex"]).index(self.max_uvindex_today)]
        # return self.max_uvindex_today,self.hour_of_max_uvindex_today

    def getmorning_ws(self):
        current_am_lower_bound = self.todaydata["time"].index(self.todaydata["time"][0])
        t11_am_upper_bound = self.todaydata["time"].index(f"{self.todays_date} 11:00")

        self.morning_ws = max(self.todaydata["wind speed"][current_am_lower_bound:t11_am_upper_bound])
        return self.morning_ws
    
    def getmiddayws(self):
        current_lower_bound = self.todaydata["time"].index(self.todaydata["time"][0])
        t3_pm_upper_bound = self.todaydata["time"].index(f"{self.todays_date} 15:00")

        self.midday_ws = max(self.todaydata["wind speed"][current_lower_bound:t3_pm_upper_bound])
        return self.midday_ws    

    def getmaxws(self):
        self.max_ws = max(self.todaydata["wind speed"])
        time_of_max_ws = self.todaydata["time"][(self.todaydata["wind speed"]).index(self.max_ws)]
        max_ws_pattern = re.compile(r'\d{2}:\d{2}')
        self.hour_of_max_ws = (max_ws_pattern.search(time_of_max_ws)).group()

        return self.max_ws,self.hour_of_max_ws

    def BackupResults(self):
        with open(f'{directory}/Weather-API-webscraper/save files/openweathermap req savefiles/{self._city} {(str(self.data["time"][0])).replace(":","H",1).replace(":","M",1)}S.txt',"w") as file:
            #current data
            file.write(f"City:{self._city}")# in {self._cityinfo}\n\n")
            file.write(f"unix time:{self.unixtime_list[0]}\n")
            for item in self.data:
                if item == "precip" or item == "wind gust":
                    pass
                else:
                    file.write(f"{item}:{self.data[item][0]}\n")
            
            file.write("\n\n")
            

            #Extra data
            file.write("Additional Info:\n" + "-"*40 + "\n")
            file.write(f"Today's Max UVindex: {self.max_uvindex_today} at {self.hour_of_max_uvindex_today}\n")
            file.write(f"Daytime Windspeed High: {self.max_ws}mph at {self.hour_of_max_ws}")
#            file.write(f"")


            file.write("\n\n\n")


            #hourly data
            file.write("Hourly:\n" + "-"*40 + "\n")
            n=1

            while n!=len(self.todaydata["time"]): #self.data or self.todaydata if you only want todays info
                file.write(f"unix time:{self.unixtime_list[n]}\n")
                for item in self.data:
                    if item == "precip" or item == "wind gust":
                        file.write(f"{item}:{self.data[item][n-1]}\n")
                    else:
                        file.write(f"{item}:{self.data[item][n]}\n")
                file.write("\n")
                n+=1
            

            
            file.write("\n\nAPI Results:\n")
            file.write("-"*80 + "\n")
            file.write(self._doc)


    def default_message(self):
        message = "\n\
            "
        
        print(message)




test_object = OpenWeatherMap()
test_object.defaultlocation()
doc = test_object.OWMap_getrequest()
test_object.getspecifiedinfo(["temp","feels like","humidity","uv index","clouds","visibility","wind speed","wind dir","wind gust","precip"])
test_object.gettodaysindex()
test_object.gettomorrowshoursindex()
test_object.gettodaymaxuvindex()
test_object.getmaxws()
test_object.BackupResults()



#hourly file writing debugging
                # file.write(f"temp: {self.data['temp'][n]}\n")
                # file.write(f"feels like: {self.data['feels like'][n]}\n")
                # file.write(f"precip: {self.data['precip'][n-1]}\n")
                # file.write(f"humidity: {self.data['humidity'][n]}\n")
                # file.write(f"uvindex: {self.data['uvindex'][n]}\n")
                # file.write(f"clouds: {self.data['clouds'][n]}\n")
                # file.write(f"visibility: {self.data['visibility'][n]}\n")
                # file.write(f"wind speed: {self.data['wind speed'][n]}\n")
                # file.write(f"wind deg: {self.data['wind deg'][n]}\n")
                # file.write(f"wind gust: {self.data['wind gust'][n-1]}\n")