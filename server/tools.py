from pprint import pprint

import httpx

from core.settings import settings


def get_weather(location: str) -> dict:
    """
    Get a string summary of current weather data for a given location.

    Args:
        location (str): City name, e.g., "London" or "London,UK"

    Returns:
        dict: A dictionary containing weather information including:
            - location (str): Location name
            - temperature (str): Current temperature in Celsius
            - feels_like (str): Feels like temperature in Celsius
            - humidity (str): Humidity percentage
            - description (str): Weather condition description
            - wind_speed (str): Wind speed in m/s
            - pressure (str): Atmospheric pressure in hPa
    """
    try:
        # Construct API URL
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': location,
            'appid': settings.OPENWEATHERMAP_API_KEY,
            'units': 'metric',  # Use 'imperial' for Fahrenheit
        }

        # Make API request using httpx
        with httpx.Client() as client:
            response = client.get(base_url, params=params)
            response.raise_for_status()  # Raise exception for bad status codes

        # Parse response
        data = response.json()

        # Create weather summary string
        weather_summary = {
            'location': f'{data["name"]}, {data["sys"]["country"]}',
            'temperature': f'{data["main"]["temp"]}°C',
            'feels_like': f'{data["main"]["feels_like"]}°C',
            'humidity': f'{data["main"]["humidity"]}%',
            'description': data['weather'][0]['description'],
            'wind_speed': f'{data["wind"]["speed"]} m/s',
            'pressure': f'{data["main"]["pressure"]} hPa',
        }

        pprint(weather_summary)

        return weather_summary

    except httpx.HTTPStatusError as http_err:
        return f'Error: HTTP error occurred: {http_err}'
    except httpx.RequestError as req_err:
        return f'Error: Failed to fetch weather data: {req_err}'
    except KeyError as key_err:
        return f'Error: Invalid response format: {key_err}'
