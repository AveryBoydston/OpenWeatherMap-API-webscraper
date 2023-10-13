import sys, re, requests
from datetime import datetime
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
import Private.WeatherAPI_private as i
#----------------------------------------------------------------------------

class OpenWeatherMap:
    def __init__(self):
        privatekey = i.OWMapKey()
        self.__key = privatekey.getkey()
        self.saveFolder = f"{directory}/Weather_API_webscraper/save files/openweathermap req savefiles" #save folder for API results
        self.currentTime = datetime.now().strftime("%m-%d-%Y %I.%M%p") #used for naming save file

    def getkey(self):
        return self.__key

    def chooselocation(self): #getlocation file
        from getlocation import latitude,longitude,city,cityinfo
        self._city = city
        self._cityinfo = cityinfo
        self._lat = latitude
        self._long = longitude

    def defaultlocation(self): #personal use
        privatelocation = i.DefaultLocation()
        self._location = privatelocation.getLocation()

        self._long, self._lat = self._location[0], self._location[1]
        self._city = self._location[2]

    def OWMap_getrequest(self):
        self._url = f"https://api.openweathermap.org/data/3.0/onecall?lat={self._lat}&lon={self._long}&exclude=daily,minutely,alerts&units=imperial&appid={self.getkey()}"
        req = requests.get(self._url)
        if req.status_code == 200:
            self._doc = req.json() #not using BeautifulSoup4 due to the formatting of the API results
        else:
            print(f"An error occurred when sending a get request to OpenWeatherMap's api. Error code: {req.status_code}")
            quit()
        
    def getspecifiedinfo(self,info):
        '''apiterms dictionary converts inputted terms to accessible terms in the API results. The file write
            portion saves the next 48 hours of selected data to a local savefile in a predetermined save location.'''
        apiterms = {
            "temp" : "temp",
            "feels like" : "feels_like",
            "humidity": "humidity",
            "precip" : "pop",
            "clouds" : "clouds",
            "visibility" : "visibility",
            "wind speed" : "wind_speed",
            "wind dir" : "wind_deg",
            "wind gust" : "wind_gust",
            "uv index" : "uvi"
        }

        with open(f'{self.saveFolder}/{self._city} {self.currentTime}.txt',"w") as file:
            file.write(f"City: {self._city}\n")# in {cityinfo}\n\n")
            file.write(f"Current time: {datetime.now().strftime('%D %I:%M%p')}\n\n")

            #hourly data
            file.write("Hourly Data:\n" + '-'*40 + '\n')
            file.write("Temperature in Farenheit (F)\n")
            file.write("Wind Speed in miles per hour (mph)\n" + '-'*40 + '\n')

            for n in range(0,48): #48 hours of hourly data
                file.write(f"unix time:{self._doc['hourly'][n]['dt']}\n")
                file.write(f"datetime:{datetime.fromtimestamp(self._doc['hourly'][n]['dt'])}\n")

                for item in info:
                    file.write(f"{item}:{self._doc['hourly'][n][apiterms[item]]}\n")
                file.write("\n")


    def today_and_tmrw_hours_index(self):
        self.current_hour = datetime.fromtimestamp(self._doc['current']['dt']).strftime("%H") #only returns the hour value
        self.today_remaining_hours = 24 - int(self.current_hour) #length/last index for remaining today's hours
        self.tmrw_11pm = self.today_remaining_hours+23

    def find_max_value_and_index(data, property_name, start_index, end_index):
        max_value = max(data[i][property_name] for i in range(start_index, end_index))
        max_index = next(i for i in range(start_index, end_index) if data[i][property_name] == max_value)
        return max_value, max_index

    def get_data(self, property_name, start_index, end_index, target_variable, data):
        max_value, max_index = OpenWeatherMap.find_max_value_and_index(data, property_name, start_index, end_index)
        setattr(self, target_variable, max_value)
        setattr(self, f'index_of_{target_variable}', max_index)
        setattr(self, f'hour_of_{target_variable}', datetime.fromtimestamp(data[max_index]['dt']))

    def gettemperature(self):
        self.get_data('temp', 0, self.today_remaining_hours - 3, 'temperature', self._doc['hourly'])

    def getfeels_like(self):
        self.get_data('feels_like', 0, self.today_remaining_hours - 3, 'feels_like', self._doc['hourly'])

    def gettodaymaxuvindex(self):
        self.get_data('uvi', 0, self.today_remaining_hours + 1, 'max_uvindex_today', self._doc['hourly'])

    def getmorning_ws(self):
        self.get_data('wind_speed', 0, self.today_remaining_hours - 11, 'morning_ws', self._doc['hourly'])

    def getmiddayws(self):
        self.get_data('wind_speed', 0, self.today_remaining_hours - 6, 'midday_ws', self._doc['hourly'])

    def getmaxws(self):
        self.get_data('wind_speed', 0, self.today_remaining_hours + 1, 'max_ws', self._doc['hourly'])

    def getwind_gust(self):
        self.get_data('wind_gust', 0, self.today_remaining_hours - 6, 'wind_gust', self._doc['hourly'])

    def get_midday_wind_gust(self):
        self.get_data('wind_gust', self.today_remaining_hours - 12, self.today_remaining_hours - 6, 'midday_wgust', self._doc['hourly'])

    def getprecip(self):
        self.get_data('pop', 0, self.today_remaining_hours - 6, 'precip', self._doc['hourly'])

    '''
    #functions to get different pieces of data. Each have their own ranges of times throughout the day, hence separate functions
    def gettemperature(self): #current hour to 7pm (19:00)
        self.temperature = max(self._doc['hourly'][i]['temp'] for i in range(0,self.today_remaining_hours-3))

        #finding index & hour of max temp
        temp = 0
        self.index_of_temperature = 0
        for i in range(0,self.today_remaining_hours-3):
            temp = self._doc['hourly'][i]['temp']
            if temp == self.temperature:
                break
            self.index_of_temperature += 1
        self.hour_of_temperature = datetime.fromtimestamp(self._doc['hourly'][self.index_of_temperature]['dt'])
 
    def getfeels_like(self): #current hour to 7pm (19:00)
        self.feels_like = max(self._doc['hourly'][i]['feels_like'] for i in range(0,self.today_remaining_hours-3))

        #finding index & hour of max feels like
        feels = 0
        self.index_of_feels_like = 0
        for i in range(0,self.today_remaining_hours-3):
            feels = self._doc['hourly'][i]['feels_like']
            if feels == self.feels_like:
                break
            self.index_of_feels_like += 1
        
        self.hour_of_feels_like = datetime.fromtimestamp(self._doc['hourly'][self.index_of_feels_like]['dt'])


    def gettodaymaxuvindex(self): #all day
        self.max_uvindex_today = max([self._doc['hourly'][i]['uvi'] for i in range(0,self.today_remaining_hours+1)]) #range function excludes 00:00 of next day

        #finding index & hour of max uvindex
        uv = 0
        self.index_of_max_uvindex_today = 0
        for i in range(0,self.today_remaining_hours+1):
            uv = self._doc['hourly'][i]['uvi']
            if uv == self.max_uvindex_today:
                break
            self.index_of_max_uvindex_today += 1

        self.hour_of_max_uvindex_today = datetime.fromtimestamp(self._doc['hourly'][self.index_of_max_uvindex_today]['dt'])


    def getmorning_ws(self): #current hour to 11am (11:00) #changed time max limit
        self.morning_ws = max([self._doc['hourly'][i]['wind_speed'] for i in range(0,self.today_remaining_hours-11)])

        #finding index & hour of morning windspeed
        ws = 0
        self.index_of_morning_ws = 0
        for i in range(0,self.today_remaining_hours-11):
            ws = self._doc['hourly'][i]['wind_speed']
            if ws == self.morning_ws:
                break
            self.index_of_morning_ws += 1

        self.hour_of_morning_ws = datetime.fromtimestamp(self._doc['hourly'][self.index_of_morning_ws]['dt'])


    def getmiddayws(self): #current hour to 5pm (17:00)
        self.midday_ws = max([self._doc['hourly'][i]['wind_speed'] for i in range(0,self.today_remaining_hours-6)])

        #finding index & hour of first occurence of midday windspeed
        ws = 0
        self.index_of_midday_ws = 0
        for i in range(0,self.today_remaining_hours-6):
            ws = self._doc['hourly'][i]['wind_speed']
            if ws == self.midday_ws:
                break
            self.index_of_midday_ws += 1

        self.hour_of_midday_ws = datetime.fromtimestamp(self._doc['hourly'][self.index_of_midday_ws]['dt'])


    def getmaxws(self): #all day
        self.max_ws = max([self._doc['hourly'][i]['wind_speed'] for i in range(0,self.today_remaining_hours+1)])

        #finding index & hour of first occurence of max windspeed
        ws = 0
        self.index_of_max_ws = 0
        for i in range(0,self.today_remaining_hours+1):
            ws = self._doc['hourly'][i]['wind_speed']
            if ws == self.max_ws:
                break
            self.index_of_max_ws += 1

        self.hour_of_max_ws = datetime.fromtimestamp(self._doc['hourly'][self.index_of_max_ws]['dt'])


    def getwind_gust(self): #current hour to 5pm (17:00)
        self.wind_gust = max([self._doc['hourly'][i]['wind_gust'] for i in range(0,self.today_remaining_hours-6)])

        #finding index & hour of first occurence of wind gust value
        gust = 0
        self.index_of_wind_gust = 0
        for i in range(0,self.today_remaining_hours-6):
            gust = self._doc['hourly'][i]['wind_gust']
            if gust == self.wind_gust:
                break
            self.index_of_wind_gust += 1

        self.hour_of_wind_gust = datetime.fromtimestamp(self._doc['hourly'][self.index_of_wind_gust]['dt'])
    
    def get_midday_wind_gust(self): #11am to 5pm. Only excecute if 11am exists in data. otherwise execute regular wind_gust
        self.midday_wgust = max([self._doc['hourly'][i]['wind_gust'] for i in range(self.today_remaining_hours-12,self.today_remaining_hours-6)])

        #finding index & hour of first occurence of midday wind gust value
        wgust = 0
        self.index_of_midday_wgust = 0
        for i in range(self.today_remaining_hours-12,self.today_remaining_hours-6):
            wgust = self._doc['hourly'][i]['wind_gust']
            if wgust == self.wind_gust:
                break
            self.index_of_midday_wgust += 1

        self.hour_of_midday_wgust = datetime.fromtimestamp(self._doc['hourly'][self.index_of_midday_wgust]['dt'])


    def getprecip(self): #current hour to 5pm
        self.precip = max([self._doc['hourly'][i]['pop'] for i in range(0,self.today_remaining_hours-6)])

        #finding index & hour of first occurence of precipitation high
        pop = 0
        self.index_of_precip = 0
        for i in range(0,self.today_remaining_hours-6):
            pop = self._doc['hourly'][i]['pop']
            if pop == self.precip:
                break
            self.index_of_precip += 1

        self.hour_of_precip = datetime.fromtimestamp(self._doc['hourly'][self.index_of_precip]['dt'])
    '''
    def convertTime(time):
        '''convert 24-hour format  to 12-hour format with am/pm. Not using datetime formatting because I don't like it.'''
        if int(time.strftime('%H')) > 12: #afternoon
            return f"{int(time.strftime('%H')) - 12}pm"
        else:
            return f"{int(time.strftime('%H'))}am"

    def BackupResults(self):
        with open(f'{self.saveFolder}/{self._city} {self.currentTime}.txt',"a") as file:

            #---- Saving Results ----
            #Temperature, UVindex
            file.write("\nAdditional Info:\n" + "-"*40 + "\n")
            file.write(f"Today's High (F): {self.temperature} at {OpenWeatherMap.convertTime(self.hour_of_temperature)}\n")
            file.write(f"Feels Like: {self.feels_like} at {OpenWeatherMap.convertTime(self.hour_of_feels_like)}\n")
            file.write(f"Today's Max UVindex: {self.max_uvindex_today} at {OpenWeatherMap.convertTime(self.hour_of_max_uvindex_today)}\n")
            
            #Wind Speed
            if self.today_remaining_hours-12 > 0: #if 11am data exists
                file.write(f"Max morning windspeed (7-11am): {self.morning_ws} at {OpenWeatherMap.convertTime(self.hour_of_morning_ws)}\n")
            else:
                file.write("It is already past 11am. No morning windspeed data.\n")

            if self.today_remaining_hours-6 > 0: #if 5pm data exists
                file.write(f"Mid-day windspeed (11am-5pm): {self.midday_ws} at {OpenWeatherMap.convertTime(self.hour_of_midday_ws)}\n")
            else:
                file.write(f"current hour past 5pm: {self.current_hour}. No mid-day windspeed data.\n")
            file.write(f"Today's Max Wind Speed: {self.max_ws} at {OpenWeatherMap.convertTime(self.hour_of_max_ws)}\n")

            #Wind gust
            if self.today_remaining_hours-12 > 0:
                file.write(f"Mid-day, Expect wind gusts of up to {self.midday_wgust} at {OpenWeatherMap.convertTime(self.hour_of_midday_wgust)}\n")
            else:
                file.write(f"Expect wind gusts of up to {self.wind_gust} at {OpenWeatherMap.convertTime(self.hour_of_wind_gust)}\n")
            file.write(f"Max wind gust: {self.wind_gust} at {OpenWeatherMap.convertTime(self.hour_of_wind_gust)}\n")

            #Chance of Rain
            if self.precip > 0.75: #75% chance
                file.write(f"High chance of rain today: {self.precip} at {OpenWeatherMap.convertTime(self.hour_of_precip)}\n")
            else:
                file.write(f"Don't expect rain today: {self.precip}")

            #API Results
            file.write('\n'*3)
            file.write("API Results:\n")
            file.write('-'*80 + '\n')
            file.write(str(self._doc))


    def createmessage(self): #message with all the information I want to know about.
        message= (f"High: {self.temperature}°F\n"
                  + f"Real Feel: {self.feels_like}°F\n"
                  + f"UVindex: {self.max_uvindex_today} @ {OpenWeatherMap.convertTime(self.hour_of_max_uvindex_today)}\n")

        if self.today_remaining_hours-6 > 0:
            message += f"Windspeed: {self.midday_ws}mph @ {OpenWeatherMap.convertTime(self.hour_of_midday_ws)}\n" + "\t"*2
            if self.today_remaining_hours-12 > 0: #11am to 5pm
                message += f" gusts of: {self.midday_wgust}mph @ {OpenWeatherMap.convertTime(self.hour_of_midday_wgust)}\n"
            else: #executes after 5pm
                message += f" gusts of: {self.wind_gust}mph @ {OpenWeatherMap.convertTime(self.hour_of_wind_gust)}\n"
            if self.midday_ws >= 15:
                message+= "Not a good day to wear certain attire.\n"
        
        if self.precip < 0.75:
            message += f"No rain. {self.precip*100}% chance\n"
        elif self.precip >= 0.90:
            message += f"Rain today at {OpenWeatherMap.convertTime(self.hour_of_precip)}. {self.precip*100}% chance\n"
        else: # 0.75 <= self.precip < 0.90
            message += f"might rain today at {OpenWeatherMap.convertTime(self.hour_of_precip)}. {self.precip*100}% chance\n"

        return message
