import sys
from openweathermap_api import OpenWeatherMap
from etext import send_sms_via_email
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
#from Private.WeatherAPI_private import Number
from Private.WeatherAPI_private import  PushBulletKey
from pushbullet import PushBullet

#Google changed something about their SMPT authentication, which now making it more difficult to send automated text messages through their system

def main():
    personal = PushBulletKey()
    API_KEY = personal.getAPI_KEY()
    PushBullet(API_KEY).push_note('Today', D())


def D():
    # try:
        info_i_want = ["temp","feels like","humidity","uv index","clouds","visibility","wind speed","wind dir","wind gust","precip"]

        d = OpenWeatherMap()
        d.defaultlocation()
        d.OWMap_getrequest()
        d.getspecifiedinfo(info_i_want)

        d.today_and_tmrw_hours_index()
        d.gettodaymaxuvindex()
        d.getmaxws()
        d.gettemperature()
        d.getfeels_like()
        d.getwind_gust()
        d.getprecip()
        if d.today_remaining_hours-12 > 0: #if 11am data exists
            d.getmorning_ws()
            d.get_midday_wind_gust()
        if d.today_remaining_hours-6 > 0: #if 5pm data exists
            d.getmiddayws()
        d.BackupResults()

        return d.createmessage()
    # except: #in case an error occurs, like a recursive error, don't want that messing up my computer's performance or spamming the phone carrier
    #     return "an error occurred with Weather API program. Exited"

main()
# print(D())