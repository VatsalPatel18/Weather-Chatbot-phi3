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

def restructure_forecast2(forecast_json):
    """Restructures the forecast JSON data into a nested dictionary by date and time, including the next three days."""
    current_date = datetime.now().date()
    forecast_dates = [current_date + timedelta(days=i) for i in range(1, 3)]

    structured_data = defaultdict(dict)
    
    for entry in forecast_json['list']:
        date, time = entry['dt_txt'].split()
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        if date_obj in forecast_dates:
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
    
    return {str(date): structured_data[str(date)] for date in forecast_dates}

def restructure_forecast(forecast_json):
    """Restructures the forecast JSON data into a nested dictionary by date and specific times."""
    current_date = datetime.now().date()
    forecast_dates = [current_date + timedelta(days=i) for i in range(1, 3)]
    important_hours = ['09:00:00', '12:00:00', '15:00:00', '18:00:00', '21:00:00']

    structured_data = defaultdict(dict)
    
    for entry in forecast_json['list']:
        date, time = entry['dt_txt'].split()
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        if date_obj in forecast_dates and time in important_hours:
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

    return {str(date): structured_data[str(date)] for date in forecast_dates}


def restructure_forecast3(forecast_json):
    """Restructures the forecast JSON data into a nested dictionary by date and time, including the next three days."""
    current_date = datetime.now().date()
    forecast_dates = [current_date + timedelta(days=i) for i in range(1, 4)]

    structured_data = defaultdict(dict)
    
    for entry in forecast_json['list']:
        date, time = entry['dt_txt'].split()
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        if date_obj in forecast_dates:
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
    
    return {str(date): structured_data[str(date)] for date in forecast_dates}
