from bs4 import BeautifulSoup
import requests
import re


place_into_separate_private_file = "b58b9c81654d669f620aac75a0a1d83e"
Tampa_url = f"https://api.openweathermap.org/data/3.0/onecall?lat=28.0589&lon=-82.4139&exclude=minutely,alerts&appid={place_into_separate_private_file}"
Tampa_return = requests.get(Tampa_url)
print(Tampa_return.status_code) #number designates if workign or not

Tampa_data = str(Tampa_return.content) #not an HTML format so we won't use bs4. str so we can search
print(Tampa_data,end="\n\n\n")


#finding all instances of '"uvi":'
look_for = '"uvi:"'
all_uvi = [k.start() for k in re.finditer(look_for,Tampa_data)]
print(all_uvi[0:6])



