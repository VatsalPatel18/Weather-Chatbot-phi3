import requests
from collections import defaultdict
from datetime import datetime, timedelta
import json

api_key = "c6dfc4d92a8f972d237ef696ec87b37a"

def get_weather_info(city):
    """Fetches current weather information for a city using OpenWeatherMap API."""
    
    url_current = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response_current = requests.get(url_current)
    if response_current.status_code != 200:
        return "Error: Could not fetch weather data."
    data_current = response_current.json()

    response = {
        'coordinates': data_current['coord'],
        'weather': data_current['weather'][0],
        'temperature': {
            'current': data_current['main']['temp'],
            'feels_like': data_current['main']['feels_like'],
            'min': data_current['main']['temp_min'],
            'max': data_current['main']['temp_max']
        },
        'pressure': {
            'sea_level': data_current['main'].get('sea_level', data_current['main']['pressure']),
            'ground_level': data_current['main'].get('grnd_level', data_current['main']['pressure'])
        },
        'humidity': data_current['main']['humidity'],
        'visibility': data_current['visibility'],
        'wind': data_current['wind'],
        'clouds': data_current['clouds'],
        'rain': data_current.get('rain', {}),
        'dt': data_current['dt'],
        'sys': data_current['sys'],
        'timezone': data_current['timezone'],
        'id': data_current['id'],
        'name': data_current['name'],
        'cod': data_current['cod']
    }

    return json.dumps(response, indent=2)

def get_forecast(city):
    """Fetches 5-day weather forecast for a city using OpenWeatherMap API."""
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response_forecast = requests.get(url_forecast)
    if response_forecast.status_code != 200:
        return "Error: Could not fetch forecast data."
    forecast_json = response_forecast.json()
    
    return restructure_forecast(forecast_json)

def restructure_forecast(forecast_json):
    """Restructures the forecast JSON data into a nested dictionary by date and time, excluding the current date."""
    current_date = datetime.now().date()
    next_date = current_date + timedelta(days=1)

    structured_data = defaultdict(dict)
    
    for entry in forecast_json['list']:
        date, time = entry['dt_txt'].split()
        if date != str(current_date):
            structured_data[date][time] = {
                'temperature': entry['main']['temp'],
                'feels_like': entry['main']['feels_like'],
                'temp_min': entry['main']['temp_min'],
                'temp_max': entry['main']['temp_max'],
                'pressure': entry['main']['pressure'],
                'humidity': entry['main']['humidity'],
                'weather': entry['weather'][0]['description'],
                'icon': entry['weather'][0]['icon'],
                'wind_speed': entry['wind']['speed'],
                'wind_deg': entry['wind']['deg'],
                'visibility': entry['visibility'],
                'pop': entry['pop'],
                'rain': entry['rain']['3h'] if 'rain' in entry else 0,
                'clouds': entry['clouds']['all']
            }
    
    return {str(next_date): structured_data[str(next_date)]}