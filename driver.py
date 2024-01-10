import sys
from openweathermap_api import OpenWeatherMap
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
from pushbullet import PushBullet
from Private.OWM_Weather_Notification.WeatherAPI_private import  PushBulletKey

def main():
    personal = PushBulletKey()
    API_KEY = personal.getAPI_KEY()
    PushBullet(API_KEY).push_note('Today', D())


def D():
    try:
        Info_I_Want = ["temp","feels like","humidity","uv index","clouds","visibility","wind speed","wind dir","wind gust","precip"]

        d = OpenWeatherMap()
        d.defaultlocation()
        d.OWMap_getrequest()
        d.getspecifiedinfo(Info_I_Want)
        d.today_and_tmrw_hours_index()

        if d.today_remaining_hours-12 > 0: #if 11am data exists
            d.getmorning_ws()
            d.get_midday_wind_gust()
        if d.today_remaining_hours-6 > 0: #if 5pm data exists
            d.getmiddayws()

        d.gettemperature()
        d.getfeels_like()
        d.gettodaymaxuvindex()
        d.getmaxws()
        d.getwind_gust()
        d.getprecip()

        d.BackupResults()
        return d.createMessage()
    except Exception: #in case an error occurs, like a recursive error, don't want that messing up my computer's performance or spamming the phone carrier
        return f"An error occurred with Weather API program. Program Exited"

<<<<<<< Updated upstream
        return d.createmessage()
    # except: #in case an error occurs, like a recursive error, don't want that messing up my computer's performance or spamming the phone carrier
    #     return "an error occurred with Weather API program. Exited"

main()
# print(D())
=======
main()
>>>>>>> Stashed changes
