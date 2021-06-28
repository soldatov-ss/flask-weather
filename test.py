import requests
def get_weather(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': f'{city}',
        'appid': '3e91701b1eece1277ca16b0fc889bc0d',
        'units': 'metric'
    }
    city_temp = requests.get(url, params=params)

    try:
        descr = city_temp.json()['weather'][0]['main']
        temp = city_temp.json()['main']['temp']
        return int(temp), descr
    except KeyError:
        # flash("The city doesn't exist!")
        return None

print(get_weather('kiev')[0])