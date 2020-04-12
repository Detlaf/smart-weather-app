import requests
import json

url = "https://api.weatherbit.io/v2.0/current"
api_key = "3e5551d00a2a4787a898a1ad24fefaeb"
city_name = "Saint-Petersburg"

payload = {
    'key': api_key,
    'city': city_name
}

res = requests.get(url, params=payload)
data = json.loads(res.text)

print('Relative Humidity (%) = {}'.format(data['data'][0]['rh']))
print('Pressure (mb) = {}'.format(data['data'][0]['pres']))
print('Cloud coverage (%) = {}'.format(data['data'][0]['clouds']))
print('Air quality index = {}'.format(data['data'][0]['aqi']))
print('Temperature = {}, it feels like {}'.format(data['data'][0]['temp'], data['data'][0]['app_temp']))
print('Wind speed (m/s) = {} in {} direction'.format(data['data'][0]['wind_spd'], data['data'][0]['wind_cdir_full']))
print('Snowfall (mm/hr) = {}'.format(data['data'][0]['snow']))
print('Weather = {}'.format(data['data'][0]['weather']))
