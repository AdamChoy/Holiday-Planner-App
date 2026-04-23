"""
places_scraper.py
-----------------
Fetches restaurants, tourist spots, and bars/nightclubs
for a destination using SerpAPI Google Maps engine.
Prices converted to GBP using conversion.py.

Usage:
    from backend.scraper.places_scraper import get_all_places, get_place_counts
"""

import os
from serpapi import GoogleSearch
from dotenv import load_dotenv
from backend.conversions import parse_price_to_gbp

load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

# -------------------------------------------------------------------
# Categories to search with their map pin colours and emojis
# -------------------------------------------------------------------
CATEGORIES = {
    "restaurants": {
        "query": "best restaurants",
        "color": "red",
        "emoji": "🍽️"
    },
    "tourist_spots": {
        "query": "top tourist spots",
        "color": "blue",
        "emoji": "📍"
    },
    "bars_nightlife": {
        "query": "bars and nightclubs",
        "color": "purple",
        "emoji": "🎉"
    },
}


def get_places(
    destination: str,
    category: str,
    country: str = None,
    max_results: int = 10
) -> list[dict]:
    """
    Fetches places for a single category in a destination.

    Args:
        destination:  City name e.g. "Barcelona"
        category:     One of "restaurants", "tourist_spots", "bars_nightlife"
        country:      Country name e.g. "Norway" — used for kr currency resolution
        max_results:  Max number of places to return

    Returns:
        List of place dicts with name, rating, lat, lon,
        price_level, photo, opening_hours etc.
    """
    if category not in CATEGORIES:
        raise ValueError(f"Category must be one of {list(CATEGORIES.keys())}")

    cat = CATEGORIES[category]

    params = {
        "engine":  "google_maps",
        "q":       f"{cat['query']} in {destination}",
        "type":    "search",
        "hl":      "en",
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    local_results = results.get("local_results", [])[:max_results]

    places = []
    for place in local_results:

        # GPS coordinates
        gps = place.get("gps_coordinates", {})

        # Raw price string e.g. "€20–30" or "$$"
        raw_price = place.get("price", "N/A")

        # Convert price to GBP
        price_gbp = parse_price_to_gbp(raw_price, country=country)

        # Opening hours
        hours = place.get("operating_hours", {})
        hours_list = [
            f"{day}: {time}"
            for day, time in hours.items()
        ] if hours else []

        places.append({
            "name":          place.get("title", "Unknown"),
            "category":      category,
            "emoji":         cat["emoji"],
            "color":         cat["color"],
            "rating":        place.get("rating", None),
            "reviews":       place.get("reviews", None),
            "price_level":   price_gbp,
            "address":       place.get("address", ""),
            "lat":           gps.get("latitude", None),
            "lon":           gps.get("longitude", None),
            "photo":         place.get("thumbnail", None),
            "opening_hours": hours_list,
            "description":   place.get("description", ""),
            "website":       place.get("website", "")
        })

    return places


def get_all_places(
    destination: str,
    country: str = None,
    max_per_category: int = 10
) -> dict:
    """
    Fetches all three categories for a destination in one call.
    This is the main function used by the frontend map.

    Args:
        destination:        City name e.g. "Barcelona"
        country:            Country name e.g. "Norway" for kr resolution
        max_per_category:   Max results per category

    Returns:
        Dict with all three categories and a flat combined list
    """
    print(f"[Places] Fetching all places for {destination}...")

    restaurants    = get_places(destination, "restaurants",    country, max_per_category)
    tourist_spots  = get_places(destination, "tourist_spots",  country, max_per_category)
    bars_nightlife = get_places(destination, "bars_nightlife", country, max_per_category)

    all_places = restaurants + tourist_spots + bars_nightlife

    return {
        "restaurants":    restaurants,
        "tourist_spots":  tourist_spots,
        "bars_nightlife": bars_nightlife,
        "all_places":     all_places,
        "total_count":    len(all_places)
    }


def get_place_counts(
    destination: str,
    country: str = None
) -> dict:
    """
    Returns just the counts per category.
    Used by recommender.py for scoring destinations.
    Saves API calls vs fetching full place details.

    Args:
        destination: City name e.g. "Barcelona"
        country:     Country name for kr currency resolution

    Returns:
        dict with restaurant_count, tourist_spot_count, nightlife_count
    """
    return {
        "restaurant_count":   len(get_places(destination, "restaurants",    country, 5)),
        "tourist_spot_count": len(get_places(destination, "tourist_spots",  country, 5)),
        "nightlife_count":    len(get_places(destination, "bars_nightlife", country, 5)),
    }