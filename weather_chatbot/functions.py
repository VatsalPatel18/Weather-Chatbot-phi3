import requests
from collections import defaultdict
from datetime import datetime, timedelta
import json
import pandas as pd
import threading
import time
import os
import signal

api_key = "c6dfc4d92a8f972d237ef696ec87b37a"

def shutdown():
    # Wait a bit before shutdown to allow the response to be returned
    def stop():
        time.sleep(1)
        os.kill(os.getpid(), signal.SIGTERM)  # Send SIGTERM to the current process to stop Gradio
        os._exit(0)
    threading.Thread(target=stop).start()
    return "Shutting down and closing the Gradio window..."

def get_weather_info(city):
    """Fetches current weather information for a city using OpenWeatherMap API."""
    
    url_current = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response_current = requests.get(url_current)
    if response_current.status_code != 200:
        return "Error: Could not fetch weather data."
    data_current = response_current.json()

    weather_description = data_current['weather'][0]['description']
    temperature_current = data_current['main']['temp']
    temperature_feels_like = data_current['main']['feels_like']
    temperature_min = data_current['main']['temp_min']
    temperature_max = data_current['main']['temp_max']
    pressure_sea_level = data_current['main'].get('sea_level', data_current['main']['pressure'])
    pressure_ground_level = data_current['main'].get('grnd_level', data_current['main']['pressure'])
    humidity = data_current['main']['humidity']
    visibility = data_current['visibility']
    wind_speed = data_current['wind']['speed']
    wind_deg = data_current['wind']['deg']
    clouds = data_current['clouds']['all']
    rain = data_current.get('rain', {}).get('1h', 0)
    dt = datetime.utcfromtimestamp(data_current['dt']).strftime('%Y-%m-%d %H:%M:%S')
    timezone = data_current['timezone']
    city_name = data_current['name']
    response_code = data_current['cod']

    formatted_info = (
        f"Weather: {weather_description}, "
        f"Temperature: current {temperature_current}°C, feels like {temperature_feels_like}°C, min {temperature_min}°C, max {temperature_max}°C, "
        f"Pressure: sea level {pressure_sea_level} hPa, ground level {pressure_ground_level} hPa, "
        f"Humidity: {humidity}%, "
        f"Visibility: {visibility} meters, "
        f"Wind: speed {wind_speed} m/s, deg {wind_deg}, "
        f"Clouds: {clouds}%, "
        f"Rain: {rain} mm, "
        f"Date/Time: {dt}, "
        f"Timezone: {timezone} seconds, "
        f"City Name: {city_name}, "
        f"Response Code: {response_code}"
    )

    return formatted_info
    
def get_forecast(city):
    """Fetches 2-day weather forecast for a city using OpenWeatherMap API and restructures the data into a table format."""
    url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response_forecast = requests.get(url_forecast)
    if response_forecast.status_code != 200:
        return "Error: Could not fetch forecast data."
    forecast_json = response_forecast.json()

    current_date = datetime.now().date()
    forecast_dates = [current_date + timedelta(days=i) for i in range(1, 3)]
    important_hours = ['09:00:00', '15:00:00', '21:00:00']

    data = []

    for entry in forecast_json['list']:
        date, time = entry['dt_txt'].split()
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        if date_obj in forecast_dates and time in important_hours:
            data.append({
                'Date': date,
                'Time': time,
                'Temperature': entry['main']['temp'],
                'Feels Like': entry['main']['feels_like'],
                'Temp Min': entry['main']['temp_min'],
                'Temp Max': entry['main']['temp_max'],
                'Pressure': entry['main']['pressure'],
                'Humidity': entry['main']['humidity'],
                'Weather': entry['weather'][0]['description'],
                'Icon': entry['weather'][0]['icon'],
                'Wind Speed': entry['wind']['speed'],
                'Wind Deg': entry['wind']['deg'],
                'Visibility': entry['visibility'],
                'Pop': entry['pop'],
                'Rain': entry['rain']['3h'] if 'rain' in entry else 0,
                'Clouds': entry['clouds']['all']
            })

    df = pd.DataFrame(data)
    df.set_index(['Date', 'Time'], inplace=True)
    return df