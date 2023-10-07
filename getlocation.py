#retrieves the latitude and logitude for any location
import sys
import re
import requests
from pickcomputer import directory
sys.path.insert(0, f'{directory}/')
import Private.WeatherAPI_private as i
#----------------------------------------------------------------\

class Location:
    def __init__(self):
        privatekey = i.OWMapKey()
        self.__key = privatekey.getkey()

    def getkey(self):
        return self.__key

    def getlatlong(self):
        self._city = input("Enter a city name: ").replace(" ","_")
    
        while True:
            try: #using try block since user input may not be valid
                self._cityurl = f"http://api.openweathermap.org/geo/1.0/direct?q={self._city}&appid={self.getkey()}"
                req = requests.get(self._cityurl, timeout = 20)
                if req.status_code==200:
                    pass
                if req.text == "[]":
                    raise Exception

                city_info = re.compile(r'"country":.+[^\}\]]')
                self._match = city_info.search(req.text)


                verify_ct = input(f"Is {self._city} located in {self._match.group()} correct? Enter yes or no: ").lower() 
                while verify_ct !="yes" and verify_ct !="no":
                    verify_ct = input("Please enter yes or no:").lower()
                if verify_ct == ("no"):
                    self._city = input("Enter a different city name:").replace(" ","_")
                    continue
                if verify_ct == ("yes"):
                    break

            except Exception:
                print(f"An error occurred when accessing the city's url. Recheck spelling.\
                        \nReturn Code:{req.status_code}\
                        \nReturn text: {req.text}\n")
                self._city = input("Enter a different city name:").replace(" ","_")
                continue


        lat_pattern = re.compile(r'("lat":)([-\d.]+)')
        lon_pattern = re.compile(r'("lon":)([-\d.]+)')

        self._lat = lat_pattern.search(req.text).group(2)
        self._long =  lon_pattern.search(req.text).group(2)

        return self._city,self._lat, self._long,self._match.group()

location = Location()
location.getlatlong()
city = location._city
cityinfo = location._match.group()
latitude = location._lat
longitude = location._long