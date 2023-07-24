import requests
response = requests.get('https://www.weather.com/')
print(response.status_code)