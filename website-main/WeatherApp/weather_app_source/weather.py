import requests
import os
from dotenv import load_dotenv

load_dotenv()
user_agent = os.getenv('USER_AGENT')

#make this a fxn
def get_12hr_forecast(latitude, longitude):
    failed = False

    if latitude is None or longitude is None:
        raise ValueError("Latitude and longitude must be provided.")
        failed = True

    headers = {'User-Agent' : user_agent}
    endpoint = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(endpoint, headers = headers)
    point = response.json()

    if response.status_code != 200:
        print(f"Error: Unable to fetch data from weather.gov. Status code: {response.status_code}")
        failed = True
    else:
        office = point['properties']['gridId']
        gridX = point['properties']['gridX']
        gridY = point['properties']['gridY']
        endpoint = f'https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast'
        response = requests.get(endpoint, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch forecast data. Status code: {response.status_code}")
        failed = True
    
    if failed:
        return None

    data = response.json()
    return data
