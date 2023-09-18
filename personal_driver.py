#https://www.alfredosequeida.com/blog/how-to-send-text-messages-for-free-using-python-use-python-to-send-text-messages-via-email/
#https://github.com/AlfredoSequeida/etext

from openweathermap_api import OpenWeatherMap
from etext import send_sms_via_email
import sys
from pickcomputer import directory
sys.path.insert(0, f'{directory}')
from Private.WeatherAPI_private import Number

def Driver():
    info = ["temp","feels like","uvindex","wind speed","wind gust","pop"]

    i = OpenWeatherMap()
    i.defaultlocation()
    i.OWMap_getrequest()
    i.getspecifiedinfo(info)
    i.gettodaysdate() #assigned to var to import to other files
    i.gettodaysinfo()
    i.gettodaymaxuvindex()
    i.getmorning_ws()
    i.getmiddayws()
    i.getmaxws()
    i.BackupResults()

Driver()





#--------- sending the message ---------
'''
phone_number = "316-655-1653"
message = "HI dad\ntest\nmessage"
provider = "AT&T"

sender_credentials = ("avcode2345@gmail.com", "amthqtdvdtmrveud")

send_sms_via_email(
    phone_number, message, provider, sender_credentials, subject="/"
)
'''