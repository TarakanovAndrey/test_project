import os

import requests
from dotenv import load_dotenv

load_dotenv()


OPENWEATHERMAP_KEY = os.environ.get("OPENWEATHERMAP_KEY")


def fetch_weather(city):
    url = "http://api.openweathermap.org/data/2.5/find"
    params = {'q': city, 'type': 'like',
              'units': 'metric',
              'APPID': OPENWEATHERMAP_KEY}
    try:
        response = requests.get(url=url, params=params).json()
        city_list = response['list']
        if city_list:
            for city_obj in city_list:
                if city_obj['name'] == city:
                    return {"city": city, "city_temp": city_obj['main']['temp']}
            print("Совпадений не найдено")
        else:
            print("Городов с таким названием нет в нашей базе")
    except Exception as e:
        print("Exception (find):", e)
