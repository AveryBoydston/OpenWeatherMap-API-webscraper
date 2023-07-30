import sys
import datetime
import requests
import re
import important_private as i
sys.path.insert(0, 'C:/Users/avboy/Documents/GitHub - Personal/')


class OpenWeatherMap:
    def __init__(self):
        privatefile = i.OWMapKey()
        self.__key = privatefile.getkey()

    def getkey(self):
        return self.__key

    def OWMap_getrequest(self):
        self._lat = 28.0589
        self._long = -82.4139

        self._url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self._lat}&lon={self._long}&exclude=daily,minutely,alerts&appid={self.getkey()}"
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

        #converting unicode time "dt" to readable time
        unixcode_timestamp = re.compile(r'"dt":\d{10}')
        matches = unixcode_timestamp.findall(self._doc)

        unixtime_list = [int(item.replace('"dt":','')) for item in matches]

        time_list = [] #list of readable times
        for time in unixtime_list:
            dt = datetime.datetime.fromtimestamp(time)
            time_list.append(dt)

        current_time = time_list[0]
        
        # for time in times[1:-1]:
        #     print(time)
        return current_time,time_list,unixtime_list

    def getuvindex(self):
        global uvindex_list
        uvi_pattern = re.compile(r'"uvi":\d[\d.]*')
        matches = uvi_pattern.findall(self._doc)
        uvindex_list = [(index.replace('"uvi":','')) for index in matches]
        return uvindex_list
    
    def getwindspeed(self):
        global windspeed_list
        ws_pattern = re.compile(r'"wind_speed":\d[\d.]*')
        matches = ws_pattern.findall(self._doc)
        windspeed_list = [(match.replace('"wind_speed":','')) for match in matches]
        return windspeed_list      

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
doc = test_object.OWMap_getrequest()
test_object.gettime()
test_object.OWMapResultsBackup()
test_object.getuvindex()
test_object.getwindspeed()
test_object.CleanBackupResults()











# def getlocation_latlong(self):
#     self._location = "wichita"
#     GoogleSearch = f"https://www.google.com/search?q{self._location.replace(' ','+')}+longitude+latitude"
#     GSreq = requests.get(GoogleSearch)

#     if GSreq.status_code != 200:
    #         print(f"An error occurred when sending a get request to {GoogleSearch}. Error code: {GSreq.status_code}")
    #         quit()
#     else:
            # self._GSdoc = BeautifulSoup(GSreq.text,"html.parser")

            # self.locationbackup() #saves a local copy of the HTML

            # self._div = (self._GSdoc).find_all(class_="Z0LcW t2b5Cf")
            # print(self._div)

#            return self._GSdoc,lat,long


# def locationbackup(self):
#     with open("C:/Users/avboy/Documents/GitHub - Personal/Weather-API-webscraper/save files/openweathermap req savefiles/test.txt","w") as file:
#         self._GS_HTML = (self._GSdoc).prettify()
#         file.write(self._GS_HTML)