import sys
import datetime
import requests
import re
sys.path.insert(0, 'C:/Users/avboy/Documents/GitHub - Personal/')
import important_private as i

class OpenWeatherMap:
    def __init__(self):
        privatefile = i.OWMapKey()
        self.__key = privatefile.getkey()

    def getkey(self):
        return self.__key

    # def getlatlong(self):
    #     self._city = input("Enter a city name:").replace(" ","_")
    #     while True:
    #         try: #using try block since user input may not be valid
    #             self._cityurl = f"http://api.openweathermap.org/geo/1.0/direct?q={self._city}&appid={self.getkey()}"

    #             req = requests.get(self._cityurl)
    #             if req.text == "[]":
    #                 raise Exception
    #             if req.status_code==200:
    #                 break
    #             else:
    #                 raise Exception
                   
    #         except Exception:
    #             print(f"An error occurred when accessing the city's url. Recheck spelling. ")
    #             self._city = input("Reinput the city name: ")
    #             continue

    #     city_info = re.compile(r'"country":.+[^\}\]]')
    #     while True:
    #         match = city_info.findall(req.text)
    #         verify_ct = input(f"Is {self._city} located in {match[0]} correct? Enter yes or no: ")
    #         verify_ct = verify_ct.lower()

    #         while verify_ct != ("yes" and "no"):
    #             verify_ct = input("Please enter yes or no:").lower()
    #         if verify_ct == ("no"):
    #             self._city = input("Enter a different city name:").replace(" ","_")
    #             continue
    #         elif verify_ct == ("yes"):
    #             break
    #     print("yay!")
                 
            

        



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
#test_object.getlatlong()
doc = test_object.OWMap_getrequest()
test_object.gettime()
test_object.OWMapResultsBackup()
test_object.getuvindex()
test_object.getwindspeed()
test_object.CleanBackupResults()





