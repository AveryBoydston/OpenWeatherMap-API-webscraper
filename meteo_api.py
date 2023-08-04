#https://open-meteo.com/en/docs#latitude=37.6922&longitude=-97.3375&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,visibility,windspeed_10m,winddirection_10m,windgusts_10m,uv_index&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&models=best_match
import sys
from datetime import datetime
import requests
from datetime import datetime
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
from getlocation import latitude,longitude,city,cityinfo
#----------------------------------------------------------------------------

class Meteo:
    def __init__(self):
        # latitude = 37.6922361 #for testing
        # longitude = -97.3375448
        self._url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,apparent_temperature,relativehumidity_2m,precipitation_probability,cloudcover,visibility,windspeed_10m,winddirection_10m,windgusts_10m,uv_index&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&models=best_match"

    def MeteoGetRequest(self):
        self._req = requests.get(self._url)
        if self._req.status_code == 200:
            self._doc = self._req.json()
            self._doc['hourly']['time'] = [time.replace("T"," ") for time in self._doc['hourly']['time']] #removing extra T's between date and time
            self._hourly = self._doc['hourly']
            return self._doc,self._hourly
        else:
            print(f"An error occurred when sending a get request to Meteo's api. Error code:{self._req.status_code}")
            quit()
    
    def getremaininghours(self):
        self.currenthour = datetime.now().replace(minute=0).strftime("%H:%M") #rounds down to current hour.
        self.Date_and_CurrentHour = datetime.now().replace(minute=0).strftime("%Y-%m-%d %H:%M")
        self.DaCH_index = self._hourly['time'].index(self.Date_and_CurrentHour)
        self.remaininghours = self._hourly['time'][self.DaCH_index:24] 
        return self.remaininghours


    def getspecifiedinfo(self,info):
        apiterm = {
            "temp" : "temperature_2m",
            "feels like" : "apparent_temperature",
            "humidity": "relativehumidity_2m",
            "precip" : "precipitation_probability",
            "clouds" : "cloudcover",
            "visibility" : "visibility",
            "wind speed" : "windspeed_10m",
            "wind dir" : "winddirection_10m",
            "wind gust" : "windgusts_10m",
            "uv index" : "uv_index"
        }
        
        #writing info to save file
        with open(f'{directory}/Weather-API-webscraper/save files/meteo savefiles/Meteo {city} {self.Date_and_CurrentHour.replace(":",".")}.txt',"w") as file:

            file.write(f"City: {city} in {cityinfo}\n\n")
            #hourly data
            file.write("Hourly:\n" + "-"*40 + "\n")

            n=self.DaCH_index
            while n!=24: #self.data or self._hourly['time'][self.DaCH_index:24] if you only want todays info
                file.write(f"time:{self._hourly['time'][n]}\n")
                for item in info:
                    item_api = apiterm[item]
                    file.write(f"{item}:{self._hourly[item_api][n]}\n")
                file.write("\n")
                n+=1

    def getmaxuvindex(self):
        self.max_uvindex_today = max(self._hourly['uv_index'][self.DaCH_index:24])
        return self.max_uvindex_today

    def getwindspeed(self):
        self.current_am = self.DaCH_index
        self.t11_bound= self._hourly['time'].index(f"{datetime.now().strftime('%Y-%m-%d')} 11:00")
        if self.current_am<self.t11_bound:
            self.getmorning_ws()
        if self.current_am>=self.t11_bound:
            self.getmidday_ws
        self.getmax_ws()

    def getmorning_ws(self):
        self.current_am = self.DaCH_index
        self.t8_am = self._hourly['time'].index(f"{datetime.now().strftime('%Y-%m-%d')} 08:00")
        self.t11_am = self._hourly['time'].index(f"{datetime.now().strftime('%Y-%m-%d')} 11:00")

        if self.current_am<=self.t8_am:
            self.morning_ws = max(self._hourly["windspeed_10m"][self.current_am:self.t11_am])
        elif self.t8_am<self.current_am:
            self.morning_ws = max(self._hourly["windspeed_10m"][self.t8_am:self.t11_am])
        return self.morning_ws

    def getmidday_ws(self):
        self.current_am = self.DaCH_index
        self.t11_am = self._hourly['time'].index(f"{datetime.now().strftime('%Y-%m-%d')} 11:00")
        self.t3_pm = self._hourly['time'].index(f"{datetime.now().strftime('%Y-%m-%d')} 15:00")

        if self.current_am>self.t3_pm: #if accessing past 3pm
            self.midday_ws = max(self._hourly["windspeed_10m"][self.t11_am:self.t3_pm])
        elif self.current_am>=self.t11_am: #using current time if past 11 to only access current/future info
            self.midday_ws = max(self._hourly["windspeed_10m"][self.current_am:self.t3_pm])
        elif self.t11_am>self.current_am: #if before 11
            self.midday_ws = max(self._hourly["windspeed_10m"][self.t11_am:self.t3_pm])
        return self.midday_ws

    def getmax_ws(self): #max windspeed from 8am to 11pm
        self.t8_am = self._hourly['time'].index(f"{datetime.now().strftime('%Y-%m-%d')} 08:00")
        self.max_ws = max(self._hourly["windspeed_10m"][self.t8_am:24])
        self.index_of_max_ws = self._hourly['windspeed_10m'].index(self.max_ws)
        self.time_of_max_ws = self._hourly['time'][self.index_of_max_ws]
        return self.max_ws,self.index_of_max_ws,self.time_of_max_ws


    def BackupMeteoResults(self):
        with open(f'{directory}/Weather-API-webscraper/save files/meteo savefiles/Meteo {city} {self.Date_and_CurrentHour.replace(":",".")}.txt',"a") as file:
            file.write("\nExtra Data:\n" + "-"*40 + "\n")
            file.write(f"Today's Max UV index: {self.getmaxuvindex()}\n")
            file.write(f"Morning Windspeed:{self.getmorning_ws()}mph [before 11am]\n")
            file.write(f"Mid-day Windspeed:{self.getmidday_ws()}mph [11am-3pm]\n")
            file.write(f"Today's Max Windspeed: {self.getmax_ws()[0]}mph at {self.getmax_ws()[2]}\n")
            
            file.write("\n\nAPI results:\n")
            file.write("-"*80 + "\n\n")
            file.write(str(self._doc))


a = Meteo()
a.MeteoGetRequest()
a.getremaininghours()
a.getspecifiedinfo(["temp","feels like","humidity","precip","clouds","visibility","wind speed","wind dir","wind gust","uv index"])
a.BackupMeteoResults()
