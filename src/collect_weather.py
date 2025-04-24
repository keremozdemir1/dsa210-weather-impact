import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city, date):
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    r = requests.get(BASE_URL, params=params)
    data = r.json()
    return {
        'date': date.strftime('%Y-%m-%d'),
        'temp': data['main']['temp'],
        'precipitation': data.get('rain', {}).get('1h', 0),
        'weather': data['weather'][0]['main'],
        'wind_speed': data['wind']['speed']
    }

if __name__ == '__main__':
    start = datetime(2025, 1, 1)
    end   = datetime(2025, 4, 23)
    city  = 'Istanbul,TR'
    recs  = []
    curr  = start
    while curr <= end:
        recs.append(get_weather(city, curr))
        curr += timedelta(days=1)
    pd.DataFrame(recs).to_csv('data/weather.csv', index=False)
