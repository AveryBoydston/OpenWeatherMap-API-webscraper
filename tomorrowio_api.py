import sys
from datetime import datetime
import requests
from datetime import datetime
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
#from getlocation import latitude,longitude,city,cityinfo

class TomorrowIO:
    def __init__(self):
        privatekey = i.TomorrowIOKey()
        self.__key = privatekey.getkey()

    def getkey(self):
        return self.__key
    
    def TomorrowIO_getrequest(self):
        latitude = 37.6922361 #for testing
        longitude = -97.3375448
        self._url = f"https://api.tomorrow.io/v4/weather/forecast?location={latitude},{longitude}&hourly:'1h'&apikey={self.getkey()}"

        headers = {"accept": "application/json"}
        self._req = requests.get(self._url, headers=headers)

        if self._req.status_code == 200:
            self._doc = self._req.json()
            return self._doc
        else:
            print(f"An error occurred when sending a get request to TomorrowIO's api. Error code:{self._req.status_code}")
            quit()
    
    def getspecifiedinfo(self,info):
        apiterm = {
            "temp" : "temperature",
            "feels like" : "temperatureApparent",
            "humidity": "humidity",
            "precip" : "precipitationProbability",
            "clouds" : "cloudCover",
            "visibility" : "visibility",
            "wind speed" : "windSpeed",
            "wind dir" : "windDirection",
            "wind gust" : "windGust",
            "uv index" : "uvIndex"
        }
        for item in self._doc["timelines"]["hourly"]:
            print(item['time'])


            

b = TomorrowIO()
b.TomorrowIO_getrequest()
b.getspecifiedinfo((["temp","feels like","humidity","precip","clouds","visibility","wind speed","wind dir","wind gust","uv index"]))
