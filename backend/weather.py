"""
weather.py
----------
Fetches weather data for a destination.

Smart switching logic:
- Within 5 days of travel: uses live OpenWeatherMap forecast
- More than 5 days away:   uses historical monthly averages from database

Usage:
    from backend.weather import get_weather
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL        = "https://api.openweathermap.org/data/2.5/forecast"

# ================================================================
# Temperature band definitions for weather preference matching
# Used by recommender.py to score destinations
# ================================================================
WEATHER_BANDS = {
    "cool": (5,  15),
    "warm": (16, 24),
    "hot":  (25, 45)
}


def get_weather(
    city: str,
    travel_date: str = None,
    destination_id: int = None
) -> dict:
    """
    Smart weather fetcher.
    Uses live data for near trips, historical averages for future trips.

    Args:
        city:           City name e.g. "Barcelona"
        travel_date:    Departure date "YYYY-MM-DD"
                        If None, fetches current live weather
        destination_id: Database ID for climate lookup
                        Required when travel_date is more than 5 days away

    Returns:
        dict with avg_temp, humidity, weather_description,
        forecast, source ("live" or "historical")
    """
    if travel_date:
        travel_dt    = datetime.strptime(travel_date, "%Y-%m-%d")
        days_until   = (travel_dt - datetime.today()).days
        travel_month = travel_dt.month
    else:
        days_until   = 0
        travel_month = datetime.today().month

    if days_until <= 5:
        print(f"[Weather] {city} — using live data ({days_until} days away)")
        return _get_live_weather(city)
    else:
        print(f"[Weather] {city} — using historical data (month {travel_month})")
        return _get_historical_weather(destination_id, travel_month, city)


def get_weather_band(avg_temp: float) -> str:
    """
    Returns the weather band for a given temperature.
    Used to display temperature category in the frontend.

    Args:
        avg_temp: Average temperature in °C

    Returns:
        "cool", "warm" or "hot"

    Examples:
        get_weather_band(10) -> "cool"
        get_weather_band(20) -> "warm"
        get_weather_band(30) -> "hot"
    """
    if avg_temp is None:
        return "unknown"
    for band, (low, high) in WEATHER_BANDS.items():
        if low <= avg_temp <= high:
            return band
    return "hot" if avg_temp > 24 else "cool"


def _get_live_weather(city: str) -> dict:
    """
    Fetches live current weather and 5 day forecast
    from OpenWeatherMap API.

    Args:
        city: City name e.g. "Barcelona"

    Returns:
        Full weather dict with live data and forecast
    """
    params = {
        "q":     city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang":  "en"
    }

    # --- Current weather ---
    current_response = requests.get(
        CURRENT_WEATHER_URL,
        params=params,
        timeout=10
    )
    current_response.raise_for_status()
    current = current_response.json()

    # --- 5 day forecast ---
    forecast_response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=10
    )
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    avg_temp = round(current["main"]["temp"], 1)

    return {
        # Current conditions
        "avg_temp":            avg_temp,
        "feels_like":          round(current["main"]["feels_like"], 1),
        "temp_min":            round(current["main"]["temp_min"], 1),
        "temp_max":            round(current["main"]["temp_max"], 1),
        "humidity":            current["main"]["humidity"],
        "cloudiness":          current["clouds"]["all"],
        "wind_speed":          round(current["wind"]["speed"] * 3.6, 1),
        "weather_description": current["weather"][0]["description"].title(),
        "weather_icon":        current["weather"][0]["icon"],
        "weather_band":        get_weather_band(avg_temp),

        # Location
        "city":                current["name"],
        "country":             current["sys"]["country"],
        "lat":                 current["coord"]["lat"],
        "lon":                 current["coord"]["lon"],

        # Forecast
        "forecast":            _parse_forecast(forecast_data),

        # Source flag
        "source":              "live"
    }


def _get_historical_weather(
    destination_id: int,
    month: int,
    city: str
) -> dict:
    """
    Fetches historical monthly climate average from database.
    Used when travel date is more than 5 days away.

    Args:
        destination_id: Database destination ID
        month:          Travel month number 1-12
        city:           City name for display

    Returns:
        Weather dict with historical averages
    """
    from backend.database.db import get_climate_average

    climate = get_climate_average(destination_id, month)

    if not climate:
        print(f"[Weather] No climate data found for destination_id={destination_id}, month={month}")
        return {
            "avg_temp":            None,
            "humidity":            None,
            "avg_rain_days":       None,
            "weather_description": "No data available",
            "weather_band":        "unknown",
            "city":                city,
            "forecast":            [],
            "source":              "historical"
        }

    avg_temp = climate["avg_temp"]

    return {
        "avg_temp":            avg_temp,
        "humidity":            climate["avg_humidity"],
        "avg_rain_days":       climate["avg_rain_days"],
        "weather_description": climate["description"],
        "weather_band":        get_weather_band(avg_temp),
        "city":                city,
        "forecast":            [],
        "source":              "historical"
    }


def _parse_forecast(forecast_data: dict) -> list[dict]:
    """
    Parses 5 day / 3 hour forecast data into daily summaries.

    Args:
        forecast_data: Raw forecast response from OpenWeatherMap

    Returns:
        List of daily forecast dicts ordered by date
    """
    daily = {}

    for entry in forecast_data.get("list", []):
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

    return [
        {
            "date":        date,
            "avg_temp":    round(sum(d["temps"]) / len(d["temps"]), 1),
            "min_temp":    round(min(d["temps"]), 1),
            "max_temp":    round(max(d["temps"]), 1),
            "description": d["description"],
            "icon":        d["icon"],
            "humidity":    d["humidity"],
            "wind_speed":  d["wind_speed"]
        }
        for date, d in daily.items()
    ]