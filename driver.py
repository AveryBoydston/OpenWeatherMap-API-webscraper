from openweathermap_api import OpenWeatherMap
from etext import send_sms_via_email
import sys
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
from Private.WeatherAPI_private import Number

'''
def main(): #sends sms message.-
    personal = Number()
    phone_number = personal.getnumber()
    provider = personal.getprov()
    sender_credentials = personal.getcred()
    message = Driver()

    send_sms_via_email(
    phone_number, message, provider, sender_credentials, subject="/"
    )
'''

def Driver():
    try:
        inputted_info = ["temp","feels like","humidity","uv index","clouds","visibility","wind speed","wind dir","wind gust","precip"]

        driver = OpenWeatherMap()
        driver.defaultlocation()
        driver.OWMap_getrequest()
        driver.getspecifiedinfo(inputted_info)

        driver.gettodaysindex()
        driver.gettomorrowshoursindex()

        driver.gettodaymaxuvindex()
        driver.getmaxws()
        driver.gettemperature()
        driver.getfeels_like()
        driver.getwind_gust()
        driver.getprecip()
        if driver.remaining_hours_in_the_day-12 > 0: #if 11am data exists
            driver.getmorning_ws()
            driver.get_midday_wind_gust()
        if driver.remaining_hours_in_the_day-6 > 0: #if 5pm data exists
            driver.getmiddayws()
        driver.BackupResults()

        return driver.createmessage()
    except: #in case an error occurs, like a recursive error, don't want that messing up my computer's performance or spamming the phone carrier
        return "an error occurred with Weather API program. Exited"

# main()
print(Driver())