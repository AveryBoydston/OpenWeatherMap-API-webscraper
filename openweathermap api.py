import sys
from datetime import datetime
import requests
import re
sys.path.insert(0, 'C:/Users/avboy/Documents/GitHub - Personal/')
import personal_private as i

class OpenWeatherMap:
    def __init__(self):
        privatefile = i.OWMapKey()
        self.__key = privatefile.getkey()

    def getkey(self):
        return self.__key

    def getlatlong(self):
        self._city = input("Enter a city name:").replace(" ","_")
        while True:
            try: #using try block since user input may not be valid
                self._cityurl = f"http://api.openweathermap.org/geo/1.0/direct?q={self._city}&appid={self.getkey()}"

                req = requests.get(self._cityurl)
                if req.status_code==200:
                    pass
                if req.text == "[]":
                    raise Exception
                                    
                city_info = re.compile(r'"country":.+[^\}\]]')
                match = city_info.search(req.text)
                verify_ct = input(f"Is {self._city} located in {match.group()} correct? Enter yes or no: ").lower()
            
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


    def OWMap_getrequest(self):
        self._url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self._lat}&lon={self._long}&exclude=daily,minutely,alerts&units=imperial&appid={self.getkey()}"
        req = requests.get(self._url)
        if req.status_code == 200:
            self._doc = req.text #not using BeautifulSoup due to formatting of API results
            return self._doc
        else:
            print(f"An error occurred when sending a get request to OpenWeatherMap's api. Error code:{req.status_code}")
            quit()

    def OWMapResultsBackup(self):
        with open(f'C:/Users/avboy/Documents/GitHub - Personal/Weather-API-webscraper/save files/openweathermap req savefiles/OWMap {(str(current_time)).replace(":","H",1).replace(":","M",1)}S.txt',"w") as f:
            f.write(self._doc)

    def gettime(self):
        global current_time,time_list,unixtime_list

        #converting unicode time code to a readable time
        unixcode_timestamp = re.compile(r'("dt":)(\d{10})')
        matches = unixcode_timestamp.finditer(self._doc)

        unixtime_list = [match.group(2) for match in matches]

        #list of readable times
        time_list = [datetime.fromtimestamp(int(time)) for time in unixtime_list] 

        current_time = time_list[0]
        
    
        #list of today's hours remaining

        today_date_finder = re.compile(r'\d{4}-\d{2}-\d{2}')
        todays_date = today_date_finder.search(str(time_list[0]))
        
        todays_date_hours = re.compile(r'{todays_date_hours}')
#        todays_date_hours = 



        return current_time,time_list,unixtime_list


    def getuvindex(self):
        global uvindex_list
        uvi_pattern = re.compile(r'("uvi":)(\d[\d.]*)')
        matches = uvi_pattern.finditer(self._doc)
        uvindex_list = [match.group(2) for match in matches]
        return uvindex_list

    def gettodaymaxuv(self):
        pass

    def getwindspeed(self):
        global windspeed_list
        ws_pattern = re.compile(r'"wind_speed":\d[\d.]*')
        matches = ws_pattern.findall(self._doc)
        windspeed_list = [(match.replace('"wind_speed":','')) for match in matches]
        return windspeed_list      

    def getmorningws(self):
        pass

    def getmaxmiddayws(self):
        pass

    def todaymaxws(self):
        pass


    def CleanBackupResults(self):
        with open(f'C:/Users/avboy/Documents/GitHub - Personal/Weather-API-webscraper/save files/openweathermap req savefiles/Results {(str(current_time)).replace(":","H",1).replace(":","M",1)}S.txt',"w") as file:
            file.write("current:\n")
            file.write(f"unix:{str(unixtime_list[0])} datetime:{str(time_list[0])}\nuvindex: {str(uvindex_list[0])}\nwindspeed:{str(windspeed_list[0])}\n\n")
            
            file.write("hourly:\n")
            n=1
            while n!=len(time_list):
                file.write(f"unix:{str(unixtime_list[n])} datetime:{str(time_list[n])}\nuvindex:{str(uvindex_list[n])}\nwindspeed:{str(windspeed_list[n])}\n\n")
                n+=1



test_object = OpenWeatherMap()
test_object.getlatlong()
doc = test_object.OWMap_getrequest()
test_object.gettime()
test_object.OWMapResultsBackup()
test_object.getuvindex()
test_object.getwindspeed()
test_object.CleanBackupResults()
