# scraper.py
import requests
import pandas as pd

def get_live_weather(airport_code):
    try:
        # Connect to the free global METAR API
        url = f"https://aviationweather.gov/api/data/metar?ids={airport_code}&format=json"
        
        # We use a 5-second timeout so your app doesn't hang if the internet drops
        response = requests.get(url, timeout=5) 
        
        if response.status_code != 200:
            print(f"Failed to connect to API. Status code: {response.status_code}")
            return None
            
        data = response.json()
        
        if not data:
            print(f"No live data found for {airport_code}.")
            return None
            
        # Extract the most recent weather report
        latest = data[0]
        
        # Map the API's data to the EXACT column names our Scikit-Learn models expect
        scraped_data = {
            'tmpc': [float(latest.get('temp', 0))],
            # Using dewpoint as proxy if relh is missing
            'drct': [float(latest.get('wdir', 0))],
            'sknt': [float(latest.get('wspd', 0))],
            'alti': [float(latest.get('altim', 29.92))],
            # Clean up strings like "10+"
        }
        
        return pd.DataFrame(scraped_data)

    except Exception as e:
        print(f"API Error for {airport_code}: {e}")
        return None