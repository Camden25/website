from tabulate import tabulate
import pandas as pd
import numpy as np


def format_weather_data(data):
    periods = data.get('properties', {}).get('periods', [])
    formatted_data = [
        {
            "Name": period.get("name"),
            "Start Time": period.get("startTime"),
            "End Time": period.get("endTime"),
            "Temperature": f"{period.get('temperature')} {period.get('temperatureUnit')}",
            "Wind": f"{period.get('windSpeed')} {period.get('windDirection')}",
            "Short Forecast": period.get("shortForecast"),
        }
        for period in periods
    ]
    return formatted_data

def display_weather_table(data):
    formatted_data = format_weather_data(data)
    #df = pd.DataFrame(formatted_data)
    #print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
    #print(formatted_data)
    return formatted_data

def format_short_forecast(data):
    formatted_data = data.split("then")
    return formatted_data

def emoji_from_forecast(forecast):
    if "sunny" in forecast.lower():
        return "☀️"
    if "cloudy" in forecast.lower():
        if "mostly" in forecast.lower():
            return "🌥️"
        if "partly" in forecast.lower():
            return "🌤️"
        return "☁️"
    if "rain" in forecast.lower():
        return "🌧️"
    if "snow" in forecast.lower():
        return "🌨️"
    if "thunderstorm" in forecast.lower():
        return "⛈️"
    if "fog" in forecast.lower():
        return "🌫️"
    if "drizzle" in forecast.lower():
        return "💧"
    if "clear" in forecast.lower():
        return "☀️"
    if "sandy" in forecast.lower():
        return "🏜️"
    if "frost" in forecast.lower():
        return "❄️"
    
    return forecast.lower()
