import sys
from datetime import datetime
import requests
import re
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
from getlocation import latitude,longitude,city,cityinfo
#----------------------------------------------------------------------------

class OpenWeatherMap:
    def __init__(self):
        privatekey = i.OWMapKey()
        self.__key = privatekey.getkey()

    def getkey(self):
        return self.__key

    def OWMap_getrequest(self):
        self._lat = latitude
        self._long = longitude        

        self._url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self._lat}&lon={self._long}&exclude=daily,minutely,alerts&units=imperial&appid={self.getkey()}"
        req = requests.get(self._url)
        if req.status_code == 200:
            self._doc = req.text #not using BeautifulSoup due to the formatting of the API results
            return self._doc
        else:
            print(f"An error occurred when sending a get request to OpenWeatherMap's api. Error code:{req.status_code}")
            quit()


    def getspecifiedinfo(self,info):
        global time_list #needed later in code but changing var would mess other parts of code, so just used global 
        self.data = {}

        #always find time
        time_pattern = re.compile(r'("dt":)([\d.]*)')
        time_matches = time_pattern.finditer(self._doc)

        self.unixtime_list = [match.group(2) for match in time_matches]
        time_list = [str(datetime.fromtimestamp(int(unix))).replace("00:00","00") for unix in self.unixtime_list]  #converting unix to DateTime format
#                                                                    ^^removing redudant seconds=00
        self.data["time"] = time_list

        for item in info:
            if item == "precip": #changing from user input to api terms
                item = "pop"
            if item == "uvindex":
                item = "uvi"

            pattern = re.compile(rf'("{item.replace(" ","_")}":)([\d.]*)') #api pattern for info results. "{info}":{data}
            matches = pattern.finditer(self._doc)

            if item == "pop": #changing back to user input
                item = "precip"
            if item == "uvi":
                item = "uvindex"


            temp_list = [float(match.group(2)) for match in matches] 

            self.data[item] = temp_list

        return self.data,self.unixtime_list,time_list


    def gettodaysdate(self):
        global current_time
        current_time = str(self.data["time"][0]) #the first data point is current info
    #    current_time_index = self.data["time"]
        today_date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        self.todays_date = today_date_pattern.search(current_time).group()
        return self.todays_date,current_time
    
    def gettodaysinfo(self):
        #find index for all remaining hours of today 
        todaytimelist = []
        for value in self.data["time"]:
            if self.todays_date in value:
                todaytimelist.append(value)

        self.todaydata = {}
        for item in self.data:
            self.todaydata[item] = self.data[item][0:len(todaytimelist)]

        return self.todaydata

    def gettodaymaxuvindex(self):
        self.max_uvindex_today = max(self.todaydata["uvindex"])
        self.hour_of_max_uvindex_today = self.todaydata["time"][(self.todaydata["uvindex"]).index(self.max_uvindex_today)]
        return self.max_uvindex_today,self.hour_of_max_uvindex_today
    
    def choosewindspeed(self):
        if f"{self.todays_date} 11:00" in self.todaydata["time"]: #if not yet lunch time
            self.getmorning_ws()
        if f"{self.todays_date} 15:00" in self.todaydata["time"]: #if not past 3pm
            self.getmiddayws()
        self.getmaxws()


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
        with open(f'{directory}/Weather-API-webscraper/save files/openweathermap req savefiles/Results {(str(self.data["time"][0])).replace(":","H",1).replace(":","M",1)}S.txt',"w") as file:
            #current data
            file.write(f"City:{city} in {cityinfo}\n\n")
            file.write("Current Data:\n" + "-"*40 + "\n")
            file.write(f"unix time:{self.unixtime_list[0]}\n")
            for item in self.data:
                if item == "precip" or item == "wind gust":
                    pass
                else:
                    file.write(f"{item}:{self.data[item][0]}\n")
            
            file.write("\n\n")
            

            #Extra data
            file.write("Extra Data:\n" + "-"*40 + "\n")
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
            

            
            file.write("\n\nAPI results:\n")
            file.write("-"*80 + "\n\n")
            file.write(self._doc)



test_object = OpenWeatherMap()
doc = test_object.OWMap_getrequest()
test_object.getspecifiedinfo(["temp","feels like","humidity","uvindex","clouds","visibility","wind speed","wind deg","wind gust","pop"])

test_object.gettodaysdate() #assigned to var to import to other files
test_object.gettodaysinfo()
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