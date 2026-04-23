"""
hotels_scraper.py
-----------------
Fetches live hotel prices using SerpAPI's Google Hotels engine.
Returns structured hotel data for each destination.

Usage:
    from backend.scraper.hotels_scraper import get_cheapest_hotel, get_hotel_options
"""

import os
from datetime import datetime, timedelta
from serpapi import GoogleSearch
from dotenv import load_dotenv
from backend.conversions import convert_to_gbp

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")


def _parse_hotel_price(price_string: str) -> float:
    """
    Parses a hotel price string and converts to GBP.

    Args:
        price_string: Raw price string e.g. "£101", "€120", "$95"

    Returns:
        Price in GBP as float, or None if unparseable
    """
    if not price_string:
        return None
    try:
        currency = (
            "GBP" if "£" in price_string else
            "EUR" if "€" in price_string else
            "USD"
        )
        raw = float(
            price_string
            .replace("£", "")
            .replace("€", "")
            .replace("$", "")
            .replace(",", "")
            .strip()
        )
        return convert_to_gbp(raw, currency)
    except ValueError:
        return None


def get_cheapest_hotel(
    destination: str,
    check_in_date: str = None,
    check_out_date: str = None,
    adults: int = 2,
    currency: str = "GBP"
) -> dict:
    """
    Returns the cheapest available hotel for a destination.

    Args:
        destination:    City name e.g. "Barcelona"
        check_in_date:  "YYYY-MM-DD" — defaults to 4 weeks from today
        check_out_date: "YYYY-MM-DD" — defaults to 1 week after check in
        adults:         Number of guests
        currency:       Price currency (default GBP)

    Returns:
        dict with avg_hotel_per_night, hotel_name, hotel_rating,
        hotel_reviews, hotel_class, check_in_date, check_out_date
    """
    if check_in_date is None:
        check_in_date = (datetime.today() + timedelta(weeks=4)).strftime("%Y-%m-%d")
    if check_out_date is None:
        check_out_date = (datetime.today() + timedelta(weeks=5)).strftime("%Y-%m-%d")

    params = {
        "engine":         "google_hotels",
        "q":              f"hotels in {destination}",
        "check_in_date":  check_in_date,
        "check_out_date": check_out_date,
        "adults":         adults,
        "currency":       currency,
        "hl":             "en",
        "gl":             "uk",
        "api_key":        SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    properties = results.get("properties", [])

    # Filter out hotels with no price
    priced = [
        p for p in properties
        if p.get("rate_per_night", {}).get("lowest")
    ]

    if not priced:
        return {
            "avg_hotel_per_night": None,
            "hotel_name":          None,
            "hotel_rating":        None,
            "hotel_reviews":       None,
            "hotel_class":         None,
            "check_in_date":       check_in_date,
            "check_out_date":      check_out_date
        }

    # Sort by price and take cheapest
    cheapest = min(
        priced,
        key=lambda x: _parse_hotel_price(
            x["rate_per_night"]["lowest"]
        ) or float("inf")
    )

    price = _parse_hotel_price(
        cheapest.get("rate_per_night", {}).get("lowest")
    )

    return {
        "avg_hotel_per_night": price,
        "hotel_name":          cheapest.get("name"),
        "hotel_rating":        cheapest.get("overall_rating"),
        "hotel_reviews":       cheapest.get("reviews"),
        "hotel_class":         cheapest.get("hotel_class"),
        "check_in_date":       check_in_date,
        "check_out_date":      check_out_date
    }


def get_hotel_options(
    destination: str,
    check_in_date: str = None,
    check_out_date: str = None,
    adults: int = 2,
    currency: str = "GBP",
    max_results: int = 5
) -> list[dict]:
    """
    Returns multiple hotel options sorted by price.
    Used for the destination detail page.

    Args:
        destination:    City name e.g. "Barcelona"
        check_in_date:  "YYYY-MM-DD" — defaults to 4 weeks from today
        check_out_date: "YYYY-MM-DD" — defaults to 1 week after check in
        adults:         Number of guests
        currency:       Price currency (default GBP)
        max_results:    Max number of hotels to return (default 5)

    Returns:
        List of hotel dicts sorted by price ascending
    """
    if check_in_date is None:
        check_in_date = (datetime.today() + timedelta(weeks=4)).strftime("%Y-%m-%d")
    if check_out_date is None:
        check_out_date = (datetime.today() + timedelta(weeks=5)).strftime("%Y-%m-%d")

    params = {
        "engine":         "google_hotels",
        "q":              f"hotels in {destination}",
        "check_in_date":  check_in_date,
        "check_out_date": check_out_date,
        "adults":         adults,
        "currency":       currency,
        "hl":             "en",
        "gl":             "uk",
        "api_key":        SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    properties = results.get("properties", [])

    hotels = []
    for hotel in properties:
        price = _parse_hotel_price(
            hotel.get("rate_per_night", {}).get("lowest")
        )
        hotels.append({
            "name":            hotel.get("name"),
            "price_per_night": price,
            "rating":          hotel.get("overall_rating"),
            "reviews":         hotel.get("reviews"),
            "hotel_class":     hotel.get("hotel_class"),
            "description":     hotel.get("description", ""),
            "image":           hotel.get("images", [{}])[0].get("thumbnail", None)
        })

    # Filter out None prices and sort by price ascending
    hotels = [h for h in hotels if h["price_per_night"] is not None]
    hotels = sorted(hotels, key=lambda x: x["price_per_night"])

    return hotels[:max_results]