"""
recommender.py
--------------
Scores and ranks destinations based on user inputs.
Fetches live data from weather, flights, hotels and places scrapers.
Returns top 5 ranked destinations.

Usage:
    from backend.recommender import get_recommendations
"""

from backend.weather import get_weather
from backend.scraper.flights_scraper import get_cheapest_flight
from backend.scraper.hotels_scraper import get_cheapest_hotel
from backend.scraper.places_scraper import get_place_counts


# -------------------------------------------------------------------
# Scoring weights — must add up to 1.0
# -------------------------------------------------------------------
WEIGHTS = {
    "vibe":    0.40,
    "budget":  0.35,
    "weather": 0.15,
    "safety":  0.10
}


def _calculate_vibe_score(destination: dict, vibes: list[str]) -> float:
    """
    Scores how well a destination matches the user's vibe preferences.
    User can select multiple vibes — weights are split equally.

    Args:
        destination: Destination dict from database
        vibes:       List of vibes e.g. ["beach", "nightlife"]

    Returns:
        Vibe score out of 10
    """
    if not vibes:
        return 5.0  # Neutral if no vibe selected

    vibe_map = {
        "beach":     "beach_score",
        "nightlife": "nightlife_score",
        "city":      "city_score"
    }

    weight_per_vibe = 1.0 / len(vibes)
    total = 0.0

    for vibe in vibes:
        key = vibe_map.get(vibe)
        if key:
            total += destination.get(key, 5.0) * weight_per_vibe

    return round(total, 2)


def _calculate_budget_score(
    total_cost: float,
    budget: float
) -> float:
    """
    Scores how well the total trip cost fits the user's budget.
    Over budget destinations still score but are ranked lower.

    Args:
        total_cost: Total estimated trip cost in £
        budget:     User's total budget in £

    Returns:
        Budget score out of 10
    """
    if total_cost is None:
        return 3.0  # Penalise missing cost data

    if total_cost <= budget:
        # Under budget — score based on how much headroom there is
        # More budget left = slightly lower score (we want best value not cheapest)
        ratio = total_cost / budget
        return round(max(6.0, 10.0 * ratio), 2)
    else:
        # Over budget — penalise proportionally
        overspend = (total_cost - budget) / budget
        return round(max(0.0, 5.0 - (overspend * 10)), 2)


def _calculate_weather_score(avg_temp: float, min_temp: int) -> float:
    """
    Scores how well the destination temperature matches user preference.

    Args:
        avg_temp: Current average temperature in °C
        min_temp: User's minimum preferred temperature in °C

    Returns:
        Weather score out of 10
    """
    if avg_temp is None:
        return 5.0  # Neutral if no weather data

    if avg_temp >= min_temp:
        # Above minimum — bonus for warmer weather up to a point
        bonus = min((avg_temp - min_temp) / 5, 2.0)
        return round(min(10.0, 8.0 + bonus), 2)
    else:
        # Below minimum — penalise proportionally
        deficit = min_temp - avg_temp
        return round(max(0.0, 8.0 - (deficit * 1.5)), 2)


def _calculate_safety_score(safety_index: float) -> float:
    """
    Converts Numbeo safety index (0-100) to a score out of 10.

    Args:
        safety_index: Numbeo safety index e.g. 61.3

    Returns:
        Safety score out of 10
    """
    if safety_index is None:
        return 5.0
    return round(safety_index / 10, 2)


def _calculate_total_cost(
    flight_cost: float,
    hotel_per_night: float,
    avg_meal_cost: float,
    trip_length_days: int,
    num_people: int
) -> float:
    """
    Estimates total trip cost in £.

    Formula:
        flights + (hotel per night × nights) + (meals × 3 per day × days × people)

    Args:
        flight_cost:      Round trip flight cost per person in £
        hotel_per_night:  Hotel cost per night in £
        avg_meal_cost:    Average meal cost per person in £
        trip_length_days: Number of nights
        num_people:       Number of travellers

    Returns:
        Total estimated cost in £
    """
    flights = (flight_cost or 0) * num_people
    hotels  = (hotel_per_night or 0) * trip_length_days
    meals   = (avg_meal_cost or 0) * 3 * trip_length_days * num_people
    return round(flights + hotels + meals, 2)


def score_destination(
    destination: dict,
    user_inputs: dict,
    trip_length_days: int
) -> dict:
    """
    Scores a single destination against user inputs.
    Fetches live weather, flight and hotel data.

    Args:
        destination:      Destination dict from database
        user_inputs:      User preferences from home.py
        trip_length_days: Number of days calculated from dates

    Returns:
        Destination dict enriched with live data and scores
    """
    print(f"[Recommender] Scoring {destination['name']}...")

    # --- Fetch live data ---
    weather = get_weather(destination["name"])

    flight = get_cheapest_flight(
        origin_iata=user_inputs["origin_airport"],
        destination_iata=destination["iata_code"],
        departure_date=user_inputs["departure_date"],
        return_date=user_inputs["return_date"],
        adults=user_inputs["num_people"]
    )

    hotel = get_cheapest_hotel(
        destination=destination["name"],
        check_in_date=user_inputs["departure_date"],
        check_out_date=user_inputs["return_date"],
        adults=user_inputs["num_people"]
    )

    # --- Calculate total cost ---
    total_cost = _calculate_total_cost(
        flight_cost=flight.get("flight_cost"),
        hotel_per_night=hotel.get("avg_hotel_per_night"),
        avg_meal_cost=destination.get("avg_meal_cost"),
        trip_length_days=trip_length_days,
        num_people=user_inputs["num_people"]
    )

    # --- Calculate individual scores ---
    vibe_score    = _calculate_vibe_score(destination, user_inputs["vibes"])
    budget_score  = _calculate_budget_score(total_cost, user_inputs["budget"])
    weather_score = _calculate_weather_score(
        weather.get("avg_temp"), user_inputs["min_temp"]
    )
    safety_score  = _calculate_safety_score(destination.get("safety_index"))

    # --- Final weighted score ---
    final_score = round(
        vibe_score    * WEIGHTS["vibe"]   +
        budget_score  * WEIGHTS["budget"] +
        weather_score * WEIGHTS["weather"] +
        safety_score  * WEIGHTS["safety"],
        2
    )

    # --- Return enriched destination ---
    return {
        # Core identity
        "name":                destination["name"],
        "country":             destination["country"],
        "lat":                 destination["lat"],
        "lon":                 destination["lon"],
        "iata_code":           destination["iata_code"],

        # Vibe scores
        "beach_score":         destination.get("beach_score"),
        "nightlife_score":     destination.get("nightlife_score"),
        "city_score":          destination.get("city_score"),

        # Live weather
        "avg_temp":            weather.get("avg_temp"),
        "humidity":            weather.get("humidity"),
        "cloudiness":          weather.get("cloudiness"),
        "wind_speed":          weather.get("wind_speed"),
        "weather_description": weather.get("weather_description"),
        "weather_icon":        weather.get("weather_icon"),
        "forecast":            weather.get("forecast"),

        # Live flights
        "flight_cost":         flight.get("flight_cost"),
        "flight_duration_hrs": flight.get("flight_duration_hrs"),
        "stops":               flight.get("stops"),
        "airline":             flight.get("airline"),

        # Live hotels
        "avg_hotel_per_night": hotel.get("avg_hotel_per_night"),
        "hotel_name":          hotel.get("hotel_name"),
        "hotel_rating":        hotel.get("hotel_rating"),

        # Cost breakdown
        "total_cost":          total_cost,
        "is_over_budget":      total_cost > user_inputs["budget"],

        # Static data
        "avg_meal_cost":       destination.get("avg_meal_cost"),
        "safety_index":        destination.get("safety_index"),
        "currency":            destination.get("currency"),
        "language":            destination.get("language"),
        "visa_required":       destination.get("visa_required"),
        "best_time_to_visit":  destination.get("best_time_to_visit"),
        "peak_times":          destination.get("peak_times"),
        "description":         destination.get("description", ""),

        # Scores
        "vibe_score":          vibe_score,
        "budget_score":        budget_score,
        "weather_score":       weather_score,
        "safety_score":        safety_score,
        "final_score":         final_score
    }


def get_recommendations(
    destinations: list[dict],
    user_inputs: dict,
    top_n: int = 5
) -> list[dict]:
    """
    Main entry point. Scores all destinations and returns top N.

    Args:
        destinations: List of destination dicts from database
        user_inputs:  User preferences from home.py
        top_n:        Number of recommendations to return (default 5)

    Returns:
        List of top N scored destinations sorted by final_score descending
    """
    from datetime import datetime

    # Calculate trip length in days
    dep = datetime.strptime(user_inputs["departure_date"], "%Y-%m-%d")
    ret = datetime.strptime(user_inputs["return_date"],    "%Y-%m-%d")
    trip_length_days = (ret - dep).days

    print(f"[Recommender] Scoring {len(destinations)} destinations...")
    print(f"[Recommender] Trip length: {trip_length_days} days")

    # Score all destinations
    scored = []
    for destination in destinations:
        try:
            result = score_destination(destination, user_inputs, trip_length_days)
            scored.append(result)
        except Exception as e:
            print(f"[Recommender] Failed to score {destination['name']}: {e}")
            continue

    # Sort by final score descending
    scored = sorted(scored, key=lambda x: x["final_score"], reverse=True)

    return scored[:top_n]