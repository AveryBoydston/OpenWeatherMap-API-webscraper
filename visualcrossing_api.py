#https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Wichita/next7days?unitGroup=us&include=hours&key=4XMCUV7PTCXYN483R8HB9XNCH&contentType=json
import sys
from datetime import datetime
import requests
from datetime import datetime
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
from getlocation import city,cityinfo
#----------------------------------------------------------------------------

class VisualCrossing:
    def __init__(self):
        privatekey = i.VisualCrossingKey()
        self.__key = privatekey.getkey()

    def getkey(self):
        return self.__key

    def VC_getrequest(self):
        self._city = city
        self._url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self._city}/next7days?unitGroup=us&include=hours&key=4XMCUV7PTCXYN483R8HB9XNCH&contentType=json"
        response = requests.get(self._url)
        if response.status_code == 200:
            self._doc = response.json()
            self._doc_today = self._doc['days'][0]['hours']
            return self._doc
        else:
            print(f"An error occurred when sending a get request to VisualCrossing's api. Error code:{response.status_code}")
            quit()
    
    def removeseconds(self): #renaming every hour from 00:00:00 to 00:00 because redundancy
        daynum=0 
        while daynum!=8:
            hournum = 0
            while hournum!=24:
                self._doc['days'][daynum]['hours'][hournum]['datetime'] = self._doc['days'][daynum]['hours'][hournum]['datetime'].replace("00:00","00")
                hournum+=1
            daynum+=1
    
    def getremaininghours(self): #today's hours: current + remaining until 24hrs 
        self.currenthour = datetime.now().replace(minute=0).strftime("%H:%M") #rounds down to current hour.
        self.currenthour_index = datetime.now().strftime("%H")
        self.date = datetime.now().strftime("%Y-%m-%d")

        self.remaininghours_list = [self.currenthour] #adding current hour to list, will add later hours with while loop in hourcalculation
        self.remaininghours_list_no_minutes = [int(self.currenthour.replace(":00",""))]

        hourcalculation = int(self.currenthour_index)
        while hourcalculation!=23:
            hourcalculation +=1
            self.remaininghours_list.append(str(hourcalculation) + ":00") #for searching api results
            self.remaininghours_list_no_minutes.append(hourcalculation) #for finding index in other results
        return self.remaininghours_list,self.remaininghours_list_no_minutes


    def getspecifiedinfo(self,info):
        apiterms = {
            "temp" : "temp",
            "feels like" : "feelslike",
            "humidity": "humidity",
            "precip" : "precipprob",
            "clouds" : "cloudcover",
            "visibility" : "visibility",
            "wind speed" : "windspeed",
            "wind dir" : "winddir",
            "wind gust" : "windgust",
            "uv index" : "uvindex"
        }

        with open(f"{directory}/Weather-API-webscraper/save files/visual crossing savefiles/{city} {self._doc['days'][0]['datetime']} {self.remaininghours_list[0].replace(':','.')}.txt","w") as file:
            file.write(f"City: {city} in {cityinfo}\n\n")

            #hourly data
            file.write("Hourly:\n" + "-"*40 + "\n")
            daynum = 0
            while daynum!=1: #daynum!=1 for today or !=8 for a week
                hournum = 0
                while hournum!=24:
                    file.write(f"time:{self._doc['days'][daynum]['datetime']} {self._doc['days'][daynum]['hours'][hournum]['datetime']}\n")
                    for item in info:
                        file.write(f"{item}:{self._doc['days'][daynum]['hours'][hournum][apiterms[item]]}\n")
                    hournum+=1
                    file.write("\n")
                daynum+=1


    def getmaxuvindex(self):
        todaysuvindexes = []
        for hour in self.remaininghours_list_no_minutes:
            todaysuvindexes.append(self._doc['days'][0]['hours'][hour]['uvindex'])
        self.maxuvindex = max(todaysuvindexes)
        self.time_of_maxuvindex = self.remaininghours_list[todaysuvindexes.index(self.maxuvindex)].replace(f"{self.date} ","")
        return self.maxuvindex,self.time_of_maxuvindex

    def getmorning_ws(self): #windspeed
        morning_ws_list = []
        for hour in range(8,11): #8am-10am
            morning_ws_list.append(self._doc['days'][0]['hours'][hour]['windspeed'])
        self.morning_ws = max(morning_ws_list)
        return self.morning_ws
    
    def getmidday_ws(self):
        midday_ws_list = []
        for hour in range(11,16): #11am-3pm
            midday_ws_list.append(self._doc['days'][0]['hours'][hour]['windspeed'])
        self.midday_ws = max(midday_ws_list)
        return self.midday_ws

    def getmax_ws(self):
        todays_ws_list = []
        for hour in self.remaininghours_list_no_minutes:
            todays_ws_list.append(self._doc['days'][0]['hours'][hour]['windspeed'])

        self.max_ws = max(todays_ws_list)
        self.index_of_max_ws = todays_ws_list.index(self.max_ws)
        self.time_of_max_ws = self.remaininghours_list[self.index_of_max_ws]
        return self.max_ws,self.index_of_max_ws,self.time_of_max_ws
 

    def BackupVCResults(self):
        with open(f"{directory}/Weather-API-webscraper/save files/visual crossing savefiles/{city} {self._doc['days'][0]['datetime']} {self.remaininghours_list[0].replace(':','.')}.txt","a") as file:
            file.write("Additional Info:\n" + "-"*40 + "\n")
            file.write(f"Today's Max UV index: {self.getmaxuvindex()[0]} at {self.getmaxuvindex()[1]}\n")
            file.write(f"Morning Windspeed:{self.getmorning_ws()}mph [8am-10am]\n")
            file.write(f"Mid-day Windspeed:{self.getmidday_ws()}mph [11am-3pm]\n")
            file.write(f"Today's Max Windspeed: {self.getmax_ws()[0]}mph at {self.getmax_ws()[2]}\n")
            
            
            
            file.write("\n\nAPI Results:\n")
            file.write("-"*80 + "\n\n")
            file.write(str(self._doc))




c = VisualCrossing()
c.VC_getrequest()
c.removeseconds()
c.getremaininghours()
c.getspecifiedinfo(["temp","feels like","humidity","precip","clouds","visibility","wind speed","wind dir","wind gust","uv index"])
c.getmaxuvindex()
c.getmorning_ws()
c.getmidday_ws()
c.getmax_ws()
c.BackupVCResults()