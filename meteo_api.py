#https://open-meteo.com/en/docs#latitude=37.6922&longitude=-97.3375&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,visibility,windspeed_10m,winddirection_10m,uv_index&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&models=best_match
import os
import sys
from datetime import datetime
import requests
import re
import json
from datetime import datetime
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.personal_private as i
from getlocation import latitude,longitude,city,cityinfo
from bs4 import BeautifulSoup
#----------------------------------------------------------------------------

class Meteo:
    def __init__(self):
        self._url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,visibility,windspeed_10m,winddirection_10m,uv_index&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&models=best_match"
        

    def MeteoGetRequest(self):
        self._req = requests.get(self._url)
        if self._req.status_code == 200:
            self._doc = BeautifulSoup(self._req.text,"html.parser")
            # self._doc['hourly']['time'] = [time.replace("T"," ") for time in self._doc['hourly']['time']] #removing extra T's between date and time
            # self._hourly = self._doc['hourly']
            print (self._doc)
            # return self._doc,self._hourly
        else:
            print(f"An error occurred when sending a get self._request to Meteo's api. Error code:{self._req.status_code}")
            quit()
    
    def getspecifiedinfo(self,info):
#        for item in info:
        result = self._hourly[info][17]
        result = self._hourly['apparent_temperature'][17]
    
    def getremaininghours(self):
        self.currenthour = datetime.now().replace(minute=0).strftime("%H:%M") #rounds down to current hour.
        self.Date_and_CurrentHour = datetime.now().replace(minute=0).strftime("%Y-%m-%d %H:%M")
        # self.DaCH_index = self._hourly['time'].index(self.Date_and_CurrentHour)
        # remaininghours = self._hourly['time'][self.DaCH_index:23]
        # print(remaininghours)

    def BackupMeteoResults(self):
        with open(f'{directory}/Weather-API-webscraper/save files/meteo savefiles/Results temp.txt',"w") as file:
            file.write(str(self._doc))


a = Meteo()
a.MeteoGetRequest()
# a.getspecifiedinfo('temperature_2m')
# a.getremaininghours()
# a.BackupMeteoResults()
    