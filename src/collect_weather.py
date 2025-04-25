import requests
import pandas as pd
from datetime import datetime, timedelta

# 1) API anahtarını sabitliyoruz
API_KEY = 'c05e0b2e6e31217bb92cd408ad9fd5bf'

# 2) Temel URL ve parametreler
URL = "https://api.openweathermap.org/data/2.5/weather"
CITY = "Istanbul,TR"

def get_weather(date):
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric"
    }
    res = requests.get(URL, params=params)
    data = res.json()
    if res.status_code != 200 or "main" not in data:
        print(f"⚠️ {date.date()} için hata: {data.get('message', res.status_code)}")
        return None
    return {
        "date": date.strftime("%Y-%m-%d"),
        "temp": data["main"]["temp"],
        "precipitation": data.get("rain", {}).get("1h", 0),
        "weather": data["weather"][0]["main"],
        "wind_speed": data["wind"]["speed"],
    }

if __name__ == "__main__":
    rows = []
    start = datetime(2025, 1, 1)
    end   = datetime(2025, 4, 23)
    cur   = start

    while cur <= end:
        rec = get_weather(cur)
        if rec:
            rows.append(rec)
        cur += timedelta(days=1)

    df = pd.DataFrame(rows)
    df.to_csv("data/weather.csv", index=False)
    print("✅ weather.csv oluşturuldu, ilk 5 satır:\n", df.head())
