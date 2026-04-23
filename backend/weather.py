"""
weather.py
----------
Fetches current and forecast weather data for a destination
using the OpenWeatherMap API.
Temperatures returned in Celsius.

Usage:
    from backend.weather import get_weather
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL        = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(city: str) -> dict:
    """
    Fetches current weather and 5 day forecast for a city.

    Args:
        city: City name e.g. "Barcelona"

    Returns:
        dict with avg_temp, humidity, cloudiness, wind_speed,
        weather_description, forecast
    """

    # --- Current weather ---
    current_params = {
        "q":     city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",  # Celsius
        "lang":  "en"
    }

    current_response = requests.get(
        CURRENT_WEATHER_URL,
        params=current_params,
        timeout=10
    )
    current_response.raise_for_status()
    current = current_response.json()

    # --- 5 day forecast ---
    forecast_response = requests.get(
        FORECAST_URL,
        params=current_params,
        timeout=10
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    # --- Parse forecast into daily summaries ---
    forecast = _parse_forecast(forecast_data)

    return {
        # Current conditions
        "avg_temp":            round(current["main"]["temp"], 1),
        "feels_like":          round(current["main"]["feels_like"], 1),
        "temp_min":            round(current["main"]["temp_min"], 1),
        "temp_max":            round(current["main"]["temp_max"], 1),
        "humidity":            current["main"]["humidity"],
        "cloudiness":          current["clouds"]["all"],
        "wind_speed":          round(current["wind"]["speed"] * 3.6, 1),  # m/s → km/h
        "weather_description": current["weather"][0]["description"].title(),
        "weather_icon":        current["weather"][0]["icon"],

        # Location confirmation
        "city":                current["name"],
        "country":             current["sys"]["country"],
        "lat":                 current["coord"]["lat"],
        "lon":                 current["coord"]["lon"],

        # 5 day forecast
        "forecast":            forecast
    }


def _parse_forecast(forecast_data: dict) -> list[dict]:
    """
    Parses 5 day / 3 hour forecast into daily summaries.

    Args:
        forecast_data: Raw forecast response from OpenWeatherMap

    Returns:
        List of daily forecast dicts with date, avg_temp,
        description and icon
    """
    daily = {}

    for entry in forecast_data.get("list", []):
        # Extract date only (not time)
        date = entry["dt_txt"].split(" ")[0]

        if date not in daily:
            daily[date] = {
                "temps":       [],
                "description": entry["weather"][0]["description"].title(),
                "icon":        entry["weather"][0]["icon"],
                "humidity":    entry["main"]["humidity"],
                "wind_speed":  round(entry["wind"]["speed"] * 3.6, 1)
            }

        daily[date]["temps"].append(entry["main"]["temp"])

    # Build daily summary
    forecast = []
    for date, data in daily.items():
        forecast.append({
            "date":        date,
            "avg_temp":    round(sum(data["temps"]) / len(data["temps"]), 1),
            "min_temp":    round(min(data["temps"]), 1),
            "max_temp":    round(max(data["temps"]), 1),
            "description": data["description"],
            "icon":        data["icon"],
            "humidity":    data["humidity"],
            "wind_speed":  data["wind_speed"]
        })

    return forecast