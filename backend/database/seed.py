"""
seed.py
-------
Populates the database with initial destination data.
Run this once to set up the database.

Usage:
    python -m database.seed
"""

from backend.database.db import insert_destination, insert_cost_data
# ================================================================
# Seed destinations
# Vibe scores: 1-10 (10 = perfect match for that vibe)
# ================================================================
DESTINATIONS = [
    # --- Spain ---
    {
        "name":               "Barcelona",
        "country":            "Spain",
        "lat":                41.3851,
        "lon":                2.1734,
        "iata_code":          "BCN",
        "currency_code":      "EUR",
        "language":           "Spanish/Catalan",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        7.0,
        "nightlife_score":    9.0,
        "city_score":         9.0,
        "description":        ""
    },
    {
        "name":               "Ibiza",
        "country":            "Spain",
        "lat":                38.9067,
        "lon":                1.4206,
        "iata_code":          "IBZ",
        "currency_code":      "EUR",
        "language":           "Spanish",
        "visa_required":      False,
        "best_time_to_visit": "June",
        "peak_times":         "July,August",
        "beach_score":        9.0,
        "nightlife_score":    10.0,
        "city_score":         3.0,
        "description":        ""
    },
    # --- Greece ---
    {
        "name":               "Mykonos",
        "country":            "Greece",
        "lat":                37.4467,
        "lon":                25.3289,
        "iata_code":          "JMK",
        "currency_code":      "EUR",
        "language":           "Greek",
        "visa_required":      False,
        "best_time_to_visit": "June",
        "peak_times":         "July,August",
        "beach_score":        10.0,
        "nightlife_score":    9.0,
        "city_score":         4.0,
        "description":        ""
    },
    {
        "name":               "Athens",
        "country":            "Greece",
        "lat":                37.9838,
        "lon":                23.7275,
        "iata_code":          "ATH",
        "currency_code":      "EUR",
        "language":           "Greek",
        "visa_required":      False,
        "best_time_to_visit": "April",
        "peak_times":         "July,August",
        "beach_score":        4.0,
        "nightlife_score":    7.0,
        "city_score":         9.0,
        "description":        ""
    },
    # --- Portugal ---
    {
        "name":               "Lisbon",
        "country":            "Portugal",
        "lat":                38.7223,
        "lon":                -9.1393,
        "iata_code":          "LIS",
        "currency_code":      "EUR",
        "language":           "Portuguese",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        5.0,
        "nightlife_score":    8.0,
        "city_score":         9.0,
        "description":        ""
    },
    # --- Italy ---
    {
        "name":               "Rome",
        "country":            "Italy",
        "lat":                41.9028,
        "lon":                12.4964,
        "iata_code":          "FCO",
        "currency_code":      "EUR",
        "language":           "Italian",
        "visa_required":      False,
        "best_time_to_visit": "April",
        "peak_times":         "July,August",
        "beach_score":        2.0,
        "nightlife_score":    6.0,
        "city_score":         10.0,
        "description":        ""
    },
    # --- Netherlands ---
    {
        "name":               "Amsterdam",
        "country":            "Netherlands",
        "lat":                52.3676,
        "lon":                4.9041,
        "iata_code":          "AMS",
        "currency_code":      "EUR",
        "language":           "Dutch",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        2.0,
        "nightlife_score":    8.0,
        "city_score":         9.0,
        "description":        ""
    },
    # --- Czech Republic ---
    {
        "name":               "Prague",
        "country":            "Czech Republic",
        "lat":                50.0755,
        "lon":                14.4378,
        "iata_code":          "PRG",
        "currency_code":      "CZK",
        "language":           "Czech",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        1.0,
        "nightlife_score":    8.0,
        "city_score":         9.0,
        "description":        ""
    },
    # --- Hungary ---
    {
        "name":               "Budapest",
        "country":            "Hungary",
        "lat":                47.4979,
        "lon":                19.0402,
        "iata_code":          "BUD",
        "currency_code":      "HUF",
        "language":           "Hungarian",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        2.0,
        "nightlife_score":    9.0,
        "city_score":         9.0,
        "description":        ""
    },
    # --- Croatia ---
    {
        "name":               "Dubrovnik",
        "country":            "Croatia",
        "lat":                42.6507,
        "lon":                18.0944,
        "iata_code":          "DBV",
        "currency_code":      "EUR",
        "language":           "Croatian",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        9.0,
        "nightlife_score":    6.0,
        "city_score":         8.0,
        "description":        ""
    },
    # --- France ---
    {
        "name":               "Paris",
        "country":            "France",
        "lat":                48.8566,
        "lon":                2.3522,
        "iata_code":          "CDG",
        "currency_code":      "EUR",
        "language":           "French",
        "visa_required":      False,
        "best_time_to_visit": "April",
        "peak_times":         "July,August",
        "beach_score":        1.0,
        "nightlife_score":    7.0,
        "city_score":         10.0,
        "description":        ""
    },
    # --- Poland ---
    {
        "name":               "Krakow",
        "country":            "Poland",
        "lat":                50.0647,
        "lon":                19.9450,
        "iata_code":          "KRK",
        "currency_code":      "PLN",
        "language":           "Polish",
        "visa_required":      False,
        "best_time_to_visit": "May",
        "peak_times":         "July,August",
        "beach_score":        1.0,
        "nightlife_score":    7.0,
        "city_score":         8.0,
        "description":        ""
    },
]

# ================================================================
# Cost data (from Numbeo — update weekly via numbeo_scraper.py)
# avg_meal_cost in £ after conversion
# ================================================================
COST_DATA = {
    "Barcelona": {"avg_meal_cost": 14.0, "cost_of_living_index": 58.2, "safety_index": 61.3},
    "Ibiza":     {"avg_meal_cost": 18.0, "cost_of_living_index": 65.0, "safety_index": 63.0},
    "Mykonos":   {"avg_meal_cost": 20.0, "cost_of_living_index": 68.0, "safety_index": 65.0},
    "Athens":    {"avg_meal_cost": 10.0, "cost_of_living_index": 45.0, "safety_index": 58.0},
    "Lisbon":    {"avg_meal_cost": 11.0, "cost_of_living_index": 50.0, "safety_index": 66.0},
    "Rome":      {"avg_meal_cost": 14.0, "cost_of_living_index": 60.0, "safety_index": 55.0},
    "Amsterdam": {"avg_meal_cost": 16.0, "cost_of_living_index": 72.0, "safety_index": 70.0},
    "Prague":    {"avg_meal_cost": 7.0,  "cost_of_living_index": 42.0, "safety_index": 71.2},
    "Budapest":  {"avg_meal_cost": 7.0,  "cost_of_living_index": 40.0, "safety_index": 68.0},
    "Dubrovnik": {"avg_meal_cost": 13.0, "cost_of_living_index": 55.0, "safety_index": 72.0},
    "Paris":     {"avg_meal_cost": 16.0, "cost_of_living_index": 75.0, "safety_index": 52.0},
    "Krakow":    {"avg_meal_cost": 6.0,  "cost_of_living_index": 38.0, "safety_index": 70.0},
}


def seed():
    """
    Seeds the database with all destinations and cost data.
    Safe to run multiple times — uses ON CONFLICT DO NOTHING.
    """
    print("Seeding database...")

    for dest in DESTINATIONS:
        dest_id = insert_destination(dest)
        if dest_id:
            cost = COST_DATA.get(dest["name"], {})
            insert_cost_data(dest_id, cost)
            print(f"  ✅ {dest['name']}")
        else:
            print(f"  ⚠️  {dest['name']} already exists — skipped")

    print("\nDone! Database seeded successfully.")


if __name__ == "__main__":
    seed()