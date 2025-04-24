import os
import pandas as pd
import googlemaps
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

def get_congestion(date, location="Istanbul,TR"):
    res = gmaps.traffic_model(origin=location, destination=location, departure_time=date)
    return {
        'date': date.strftime('%Y-%m-%d'),
        'congestion_index': res.get('traffic_model', {}).get('congestion_level', 0)
    }

if __name__ == '__main__':
    start = datetime(2025, 1, 1)
    end   = datetime(2025, 4, 23)
    recs  = []
    curr  = start
    while curr <= end:
        recs.append(get_congestion(curr))
        curr += timedelta(days=1)
    pd.DataFrame(recs).to_csv('data/traffic.csv', index=False)
