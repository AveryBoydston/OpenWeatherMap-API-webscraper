#https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Wichita/next7days?unitGroup=us&include=hours&key=4XMCUV7PTCXYN483R8HB9XNCH&contentType=json
import sys
from datetime import datetime
import requests
from datetime import datetime
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
#from getlocation import latitude,longitude,city,cityinfo
#----------------------------------------------------------------------------

class VisualCrossing:
    def __init__(self):
        privatekey = i.VisualCrossingKey()
        self.__key = privatekey.getkey()

    def getkey(self):
        return self.__key

    def VC_getrequest(self):
        self._city = "Wichita" #city
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
    
    def getremaininghours(self):
        self.currenthour = datetime.now().replace(minute=0).strftime("%H:%M") #rounds down to current hour.
        self.currenthour_index = datetime.now().strftime("%H")
        self.date = datetime.now().strftime("%Y-%m-%d")
        #print(self.currenthour) == print(self._doc['days'][0]['hours'][int(self.currenthour_index)]['datetime'])
        
        self.remaininghours_list = [self.currenthour]

        hourcalculation = int(self.currenthour_index)
        while hourcalculation!=23:
            hourcalculation +=1
            hourcalculation = str(hourcalculation)
            hourcalculation += ":00"
            self.remaininghours_list.append(hourcalculation)
            hourcalculation = int(hourcalculation.replace(":00",""))

        return self.remaininghours_list   


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

        with open(f"{directory}/Weather-API-webscraper/save files/visual crossing savefiles/{self._doc['days'][0]['datetime']} {self.remaininghours_list[0].replace(':','.')}.txt","w") as file:
            
#            file.write(f"City: {city} in {cityinfo}\n\n")

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
                    file.write("\n\n")
                daynum+=1
            file.write("\n\n\n")
            file.write(str(self._doc))
    



c = VisualCrossing()
c.VC_getrequest()
c.removeseconds()
c.getremaininghours()
c.getspecifiedinfo(["temp","feels like","humidity","precip","clouds","visibility","wind speed","wind dir","wind gust","uv index"])