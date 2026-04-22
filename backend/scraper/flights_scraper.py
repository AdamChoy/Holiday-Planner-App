"""
flights_scraper.py
------------------
Fetches live flight prices using SerpAPI's Google Flights engine.
Returns structured flight data for each destination.
"""

import os
from datetime import datetime, timedelta
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def get_cheapest_flight(
    origin_iata: str,
    destination_iata: str,
    departure_date: str = None,
    return_date: str = None,
    adults: int = 1,
    currency: str = "GBP"
) -> dict:
    """
    Returns the cheapest available round trip flight between two airports.

    Args:
        origin_iata:      Departure airport code e.g. "LGW"
        destination_iata: Destination airport code e.g. "BCN" (Barcelona)
        departure_date:   "YYYY-MM-DD" — defaults to 4 weeks from today
        return_date:      "YYYY-MM-DD" — defaults to 2 weeks after departure
        adults:           Number of passengers
        currency:         Price currency (default GBP)

    Returns:
        dict with flight_cost, duration, stops, airline, departure_date, return_date
    """
    if departure_date is None:
        departure_date = (datetime.today() + timedelta(weeks=4)).strftime("%Y-%m-%d")

    if return_date is None:
        return_date = (datetime.today() + timedelta(weeks=6)).strftime("%Y-%m-%d")

    params = {
        "engine":        "google_flights",
        "departure_id":  origin_iata,
        "arrival_id":    destination_iata,
        "outbound_date": departure_date,
        "return_date":   return_date,
        "type":          "1",           # 1 = round trip
        "currency":      currency,
        "adults":        adults,
        "hl":            "en",
        "api_key":       SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Extract best flights first, fall back to other flights
    flights = results.get("best_flights") or results.get("other_flights", [])

    if not flights:
        return {
            "flight_cost":         None,
            "flight_duration_hrs": None,
            "stops":               None,
            "airline":             None,
            "departure_date":      departure_date,
            "return_date":         return_date
        }

    # Cheapest is first result
    cheapest = flights[0]

    price         = cheapest.get("price")
    duration_mins = cheapest.get("total_duration")
    duration_hrs  = round(duration_mins / 60, 2) if duration_mins else None
    airline       = cheapest.get("flights", [{}])[0].get("airline", "Unknown")
    stops         = len(cheapest.get("flights", [])) - 1

    return {
        "flight_cost":         price,
        "flight_duration_hrs": duration_hrs,
        "stops":               stops,
        "airline":             airline,
        "departure_date":      departure_date,
        "return_date":         return_date
    }