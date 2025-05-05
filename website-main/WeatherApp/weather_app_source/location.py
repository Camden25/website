from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

load_dotenv()
user_agent = os.getenv('USER_AGENT')

def get_location(city_name):
    geolocator = Nominatim(user_agent=user_agent)
    location = geolocator.geocode(city_name)
    if location:
        return location
    else:
        return None
