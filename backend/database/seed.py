"""
seed.py
-------
Populates the database with initial destination, airport
and climate data.
Run this once to set up the database.

Usage:
    python -m backend.database.seed
"""

from backend.database.db import get_connection, insert_destination, insert_cost_data

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

# ================================================================
# UK departure airports
# ================================================================
AIRPORTS = [
    {"name": "London Heathrow",       "iata_code": "LHR", "city": "London",     "region": "England"},
    {"name": "London Gatwick",        "iata_code": "LGW", "city": "London",     "region": "England"},
    {"name": "London Stansted",       "iata_code": "STN", "city": "London",     "region": "England"},
    {"name": "London Luton",          "iata_code": "LTN", "city": "London",     "region": "England"},
    {"name": "London City",           "iata_code": "LCY", "city": "London",     "region": "England"},
    {"name": "Manchester",            "iata_code": "MAN", "city": "Manchester", "region": "England"},
    {"name": "Birmingham",            "iata_code": "BHX", "city": "Birmingham", "region": "England"},
    {"name": "Edinburgh",             "iata_code": "EDI", "city": "Edinburgh",  "region": "Scotland"},
    {"name": "Glasgow",               "iata_code": "GLA", "city": "Glasgow",    "region": "Scotland"},
    {"name": "Bristol",               "iata_code": "BRS", "city": "Bristol",    "region": "England"},
    {"name": "Newcastle",             "iata_code": "NCL", "city": "Newcastle",  "region": "England"},
    {"name": "Leeds Bradford",        "iata_code": "LBA", "city": "Leeds",      "region": "England"},
    {"name": "Liverpool",             "iata_code": "LPL", "city": "Liverpool",  "region": "England"},
    {"name": "Belfast International", "iata_code": "BFS", "city": "Belfast",    "region": "N. Ireland"},
    {"name": "Cardiff",               "iata_code": "CWL", "city": "Cardiff",    "region": "Wales"},
]

# ================================================================
# Climate data — historical monthly averages
# Source: Climate-Data.org / Weather Atlas
# ================================================================
CLIMATE_DATA = {
    "Barcelona": {
        1:  {"avg_temp": 10, "avg_humidity": 72, "avg_rain_days": 5,  "description": "Cool and mild"},
        2:  {"avg_temp": 11, "avg_humidity": 70, "avg_rain_days": 5,  "description": "Cool and mild"},
        3:  {"avg_temp": 13, "avg_humidity": 68, "avg_rain_days": 6,  "description": "Mild"},
        4:  {"avg_temp": 16, "avg_humidity": 66, "avg_rain_days": 7,  "description": "Warm"},
        5:  {"avg_temp": 19, "avg_humidity": 65, "avg_rain_days": 6,  "description": "Warm"},
        6:  {"avg_temp": 23, "avg_humidity": 62, "avg_rain_days": 4,  "description": "Hot and sunny"},
        7:  {"avg_temp": 26, "avg_humidity": 60, "avg_rain_days": 2,  "description": "Hot and sunny"},
        8:  {"avg_temp": 26, "avg_humidity": 63, "avg_rain_days": 3,  "description": "Hot and sunny"},
        9:  {"avg_temp": 23, "avg_humidity": 67, "avg_rain_days": 5,  "description": "Warm"},
        10: {"avg_temp": 18, "avg_humidity": 70, "avg_rain_days": 7,  "description": "Mild"},
        11: {"avg_temp": 13, "avg_humidity": 72, "avg_rain_days": 6,  "description": "Cool"},
        12: {"avg_temp": 10, "avg_humidity": 73, "avg_rain_days": 5,  "description": "Cool"},
    },
    "Ibiza": {
        1:  {"avg_temp": 11, "avg_humidity": 74, "avg_rain_days": 5,  "description": "Cool"},
        2:  {"avg_temp": 12, "avg_humidity": 72, "avg_rain_days": 4,  "description": "Cool"},
        3:  {"avg_temp": 14, "avg_humidity": 70, "avg_rain_days": 5,  "description": "Mild"},
        4:  {"avg_temp": 17, "avg_humidity": 67, "avg_rain_days": 4,  "description": "Warm"},
        5:  {"avg_temp": 21, "avg_humidity": 64, "avg_rain_days": 3,  "description": "Warm"},
        6:  {"avg_temp": 25, "avg_humidity": 60, "avg_rain_days": 2,  "description": "Hot and sunny"},
        7:  {"avg_temp": 28, "avg_humidity": 57, "avg_rain_days": 1,  "description": "Hot and sunny"},
        8:  {"avg_temp": 28, "avg_humidity": 59, "avg_rain_days": 2,  "description": "Hot and sunny"},
        9:  {"avg_temp": 25, "avg_humidity": 63, "avg_rain_days": 4,  "description": "Warm"},
        10: {"avg_temp": 20, "avg_humidity": 68, "avg_rain_days": 6,  "description": "Mild"},
        11: {"avg_temp": 15, "avg_humidity": 72, "avg_rain_days": 5,  "description": "Cool"},
        12: {"avg_temp": 12, "avg_humidity": 74, "avg_rain_days": 5,  "description": "Cool"},
    },
    "Mykonos": {
        1:  {"avg_temp": 12, "avg_humidity": 73, "avg_rain_days": 8,  "description": "Cool and windy"},
        2:  {"avg_temp": 12, "avg_humidity": 72, "avg_rain_days": 7,  "description": "Cool and windy"},
        3:  {"avg_temp": 14, "avg_humidity": 70, "avg_rain_days": 6,  "description": "Mild"},
        4:  {"avg_temp": 17, "avg_humidity": 66, "avg_rain_days": 4,  "description": "Warm"},
        5:  {"avg_temp": 21, "avg_humidity": 62, "avg_rain_days": 2,  "description": "Warm and sunny"},
        6:  {"avg_temp": 26, "avg_humidity": 55, "avg_rain_days": 1,  "description": "Hot and sunny"},
        7:  {"avg_temp": 28, "avg_humidity": 52, "avg_rain_days": 0,  "description": "Hot and sunny"},
        8:  {"avg_temp": 28, "avg_humidity": 54, "avg_rain_days": 0,  "description": "Hot and sunny"},
        9:  {"avg_temp": 25, "avg_humidity": 58, "avg_rain_days": 1,  "description": "Warm and sunny"},
        10: {"avg_temp": 21, "avg_humidity": 65, "avg_rain_days": 4,  "description": "Mild"},
        11: {"avg_temp": 17, "avg_humidity": 70, "avg_rain_days": 6,  "description": "Cool"},
        12: {"avg_temp": 13, "avg_humidity": 73, "avg_rain_days": 8,  "description": "Cool"},
    },
    "Athens": {
        1:  {"avg_temp": 10, "avg_humidity": 72, "avg_rain_days": 8,  "description": "Cool"},
        2:  {"avg_temp": 11, "avg_humidity": 70, "avg_rain_days": 7,  "description": "Cool"},
        3:  {"avg_temp": 14, "avg_humidity": 67, "avg_rain_days": 6,  "description": "Mild"},
        4:  {"avg_temp": 18, "avg_humidity": 62, "avg_rain_days": 4,  "description": "Warm"},
        5:  {"avg_temp": 23, "avg_humidity": 57, "avg_rain_days": 3,  "description": "Warm and sunny"},
        6:  {"avg_temp": 28, "avg_humidity": 48, "avg_rain_days": 1,  "description": "Hot and sunny"},
        7:  {"avg_temp": 31, "avg_humidity": 44, "avg_rain_days": 0,  "description": "Very hot and sunny"},
        8:  {"avg_temp": 31, "avg_humidity": 45, "avg_rain_days": 0,  "description": "Very hot and sunny"},
        9:  {"avg_temp": 27, "avg_humidity": 52, "avg_rain_days": 1,  "description": "Hot and sunny"},
        10: {"avg_temp": 21, "avg_humidity": 62, "avg_rain_days": 5,  "description": "Mild"},
        11: {"avg_temp": 15, "avg_humidity": 69, "avg_rain_days": 7,  "description": "Cool"},
        12: {"avg_temp": 11, "avg_humidity": 72, "avg_rain_days": 8,  "description": "Cool"},
    },
    "Lisbon": {
        1:  {"avg_temp": 12, "avg_humidity": 80, "avg_rain_days": 11, "description": "Cool and rainy"},
        2:  {"avg_temp": 13, "avg_humidity": 78, "avg_rain_days": 9,  "description": "Cool"},
        3:  {"avg_temp": 15, "avg_humidity": 74, "avg_rain_days": 9,  "description": "Mild"},
        4:  {"avg_temp": 17, "avg_humidity": 70, "avg_rain_days": 8,  "description": "Warm"},
        5:  {"avg_temp": 20, "avg_humidity": 66, "avg_rain_days": 6,  "description": "Warm and sunny"},
        6:  {"avg_temp": 24, "avg_humidity": 60, "avg_rain_days": 3,  "description": "Hot and sunny"},
        7:  {"avg_temp": 27, "avg_humidity": 55, "avg_rain_days": 1,  "description": "Hot and sunny"},
        8:  {"avg_temp": 27, "avg_humidity": 57, "avg_rain_days": 2,  "description": "Hot and sunny"},
        9:  {"avg_temp": 25, "avg_humidity": 62, "avg_rain_days": 4,  "description": "Warm"},
        10: {"avg_temp": 20, "avg_humidity": 70, "avg_rain_days": 8,  "description": "Mild"},
        11: {"avg_temp": 15, "avg_humidity": 77, "avg_rain_days": 10, "description": "Cool"},
        12: {"avg_temp": 12, "avg_humidity": 80, "avg_rain_days": 11, "description": "Cool and rainy"},
    },
    "Rome": {
        1:  {"avg_temp": 8,  "avg_humidity": 75, "avg_rain_days": 7,  "description": "Cool"},
        2:  {"avg_temp": 9,  "avg_humidity": 73, "avg_rain_days": 7,  "description": "Cool"},
        3:  {"avg_temp": 12, "avg_humidity": 70, "avg_rain_days": 7,  "description": "Mild"},
        4:  {"avg_temp": 16, "avg_humidity": 66, "avg_rain_days": 6,  "description": "Warm"},
        5:  {"avg_temp": 20, "avg_humidity": 62, "avg_rain_days": 5,  "description": "Warm and sunny"},
        6:  {"avg_temp": 25, "avg_humidity": 55, "avg_rain_days": 2,  "description": "Hot and sunny"},
        7:  {"avg_temp": 28, "avg_humidity": 50, "avg_rain_days": 1,  "description": "Hot and sunny"},
        8:  {"avg_temp": 27, "avg_humidity": 52, "avg_rain_days": 2,  "description": "Hot and sunny"},
        9:  {"avg_temp": 24, "avg_humidity": 58, "avg_rain_days": 4,  "description": "Warm"},
        10: {"avg_temp": 18, "avg_humidity": 67, "avg_rain_days": 6,  "description": "Mild"},
        11: {"avg_temp": 13, "avg_humidity": 73, "avg_rain_days": 8,  "description": "Cool"},
        12: {"avg_temp": 9,  "avg_humidity": 76, "avg_rain_days": 8,  "description": "Cool"},
    },
    "Amsterdam": {
        1:  {"avg_temp": 4,  "avg_humidity": 86, "avg_rain_days": 13, "description": "Cold and grey"},
        2:  {"avg_temp": 4,  "avg_humidity": 84, "avg_rain_days": 11, "description": "Cold"},
        3:  {"avg_temp": 7,  "avg_humidity": 80, "avg_rain_days": 11, "description": "Cool"},
        4:  {"avg_temp": 11, "avg_humidity": 76, "avg_rain_days": 10, "description": "Mild"},
        5:  {"avg_temp": 15, "avg_humidity": 72, "avg_rain_days": 10, "description": "Mild and pleasant"},
        6:  {"avg_temp": 18, "avg_humidity": 71, "avg_rain_days": 10, "description": "Warm"},
        7:  {"avg_temp": 20, "avg_humidity": 72, "avg_rain_days": 10, "description": "Warm"},
        8:  {"avg_temp": 20, "avg_humidity": 73, "avg_rain_days": 10, "description": "Warm"},
        9:  {"avg_temp": 17, "avg_humidity": 77, "avg_rain_days": 11, "description": "Mild"},
        10: {"avg_temp": 12, "avg_humidity": 82, "avg_rain_days": 12, "description": "Cool"},
        11: {"avg_temp": 7,  "avg_humidity": 86, "avg_rain_days": 13, "description": "Cold"},
        12: {"avg_temp": 4,  "avg_humidity": 87, "avg_rain_days": 13, "description": "Cold and grey"},
    },
    "Prague": {
        1:  {"avg_temp": 0,  "avg_humidity": 82, "avg_rain_days": 10, "description": "Cold and snowy"},
        2:  {"avg_temp": 2,  "avg_humidity": 79, "avg_rain_days": 9,  "description": "Cold"},
        3:  {"avg_temp": 7,  "avg_humidity": 74, "avg_rain_days": 9,  "description": "Cool"},
        4:  {"avg_temp": 12, "avg_humidity": 68, "avg_rain_days": 9,  "description": "Mild"},
        5:  {"avg_temp": 17, "avg_humidity": 67, "avg_rain_days": 11, "description": "Warm"},
        6:  {"avg_temp": 20, "avg_humidity": 68, "avg_rain_days": 11, "description": "Warm"},
        7:  {"avg_temp": 22, "avg_humidity": 67, "avg_rain_days": 10, "description": "Warm and sunny"},
        8:  {"avg_temp": 22, "avg_humidity": 67, "avg_rain_days": 10, "description": "Warm and sunny"},
        9:  {"avg_temp": 18, "avg_humidity": 71, "avg_rain_days": 8,  "description": "Mild"},
        10: {"avg_temp": 12, "avg_humidity": 77, "avg_rain_days": 9,  "description": "Cool"},
        11: {"avg_temp": 5,  "avg_humidity": 82, "avg_rain_days": 10, "description": "Cold"},
        12: {"avg_temp": 1,  "avg_humidity": 84, "avg_rain_days": 11, "description": "Cold and snowy"},
    },
    "Budapest": {
        1:  {"avg_temp": 1,  "avg_humidity": 80, "avg_rain_days": 9,  "description": "Cold"},
        2:  {"avg_temp": 4,  "avg_humidity": 76, "avg_rain_days": 8,  "description": "Cold"},
        3:  {"avg_temp": 9,  "avg_humidity": 70, "avg_rain_days": 8,  "description": "Cool"},
        4:  {"avg_temp": 15, "avg_humidity": 64, "avg_rain_days": 8,  "description": "Mild"},
        5:  {"avg_temp": 20, "avg_humidity": 63, "avg_rain_days": 9,  "description": "Warm"},
        6:  {"avg_temp": 23, "avg_humidity": 63, "avg_rain_days": 9,  "description": "Warm and sunny"},
        7:  {"avg_temp": 25, "avg_humidity": 61, "avg_rain_days": 7,  "description": "Hot and sunny"},
        8:  {"avg_temp": 25, "avg_humidity": 61, "avg_rain_days": 7,  "description": "Hot and sunny"},
        9:  {"avg_temp": 20, "avg_humidity": 66, "avg_rain_days": 6,  "description": "Warm"},
        10: {"avg_temp": 14, "avg_humidity": 73, "avg_rain_days": 7,  "description": "Cool"},
        11: {"avg_temp": 7,  "avg_humidity": 79, "avg_rain_days": 9,  "description": "Cold"},
        12: {"avg_temp": 2,  "avg_humidity": 81, "avg_rain_days": 10, "description": "Cold"},
    },
    "Dubrovnik": {
        1:  {"avg_temp": 9,  "avg_humidity": 73, "avg_rain_days": 11, "description": "Cool"},
        2:  {"avg_temp": 10, "avg_humidity": 71, "avg_rain_days": 10, "description": "Cool"},
        3:  {"avg_temp": 12, "avg_humidity": 68, "avg_rain_days": 9,  "description": "Mild"},
        4:  {"avg_temp": 16, "avg_humidity": 64, "avg_rain_days": 7,  "description": "Warm"},
        5:  {"avg_temp": 20, "avg_humidity": 61, "avg_rain_days": 5,  "description": "Warm and sunny"},
        6:  {"avg_temp": 24, "avg_humidity": 56, "avg_rain_days": 3,  "description": "Hot and sunny"},
        7:  {"avg_temp": 27, "avg_humidity": 53, "avg_rain_days": 1,  "description": "Hot and sunny"},
        8:  {"avg_temp": 27, "avg_humidity": 54, "avg_rain_days": 2,  "description": "Hot and sunny"},
        9:  {"avg_temp": 23, "avg_humidity": 59, "avg_rain_days": 5,  "description": "Warm"},
        10: {"avg_temp": 18, "avg_humidity": 66, "avg_rain_days": 8,  "description": "Mild"},
        11: {"avg_temp": 13, "avg_humidity": 71, "avg_rain_days": 11, "description": "Cool"},
        12: {"avg_temp": 10, "avg_humidity": 74, "avg_rain_days": 12, "description": "Cool"},
    },
    "Paris": {
        1:  {"avg_temp": 5,  "avg_humidity": 82, "avg_rain_days": 11, "description": "Cold and grey"},
        2:  {"avg_temp": 6,  "avg_humidity": 79, "avg_rain_days": 9,  "description": "Cold"},
        3:  {"avg_temp": 10, "avg_humidity": 74, "avg_rain_days": 10, "description": "Cool"},
        4:  {"avg_temp": 13, "avg_humidity": 70, "avg_rain_days": 9,  "description": "Mild"},
        5:  {"avg_temp": 17, "avg_humidity": 68, "avg_rain_days": 10, "description": "Warm"},
        6:  {"avg_temp": 21, "avg_humidity": 65, "avg_rain_days": 8,  "description": "Warm and sunny"},
        7:  {"avg_temp": 23, "avg_humidity": 63, "avg_rain_days": 7,  "description": "Warm and sunny"},
        8:  {"avg_temp": 23, "avg_humidity": 64, "avg_rain_days": 7,  "description": "Warm and sunny"},
        9:  {"avg_temp": 19, "avg_humidity": 68, "avg_rain_days": 8,  "description": "Mild"},
        10: {"avg_temp": 14, "avg_humidity": 75, "avg_rain_days": 10, "description": "Cool"},
        11: {"avg_temp": 8,  "avg_humidity": 81, "avg_rain_days": 11, "description": "Cold"},
        12: {"avg_temp": 5,  "avg_humidity": 83, "avg_rain_days": 11, "description": "Cold and grey"},
    },
    "Krakow": {
        1:  {"avg_temp": -1, "avg_humidity": 83, "avg_rain_days": 10, "description": "Cold and snowy"},
        2:  {"avg_temp": 1,  "avg_humidity": 80, "avg_rain_days": 9,  "description": "Cold"},
        3:  {"avg_temp": 6,  "avg_humidity": 75, "avg_rain_days": 9,  "description": "Cool"},
        4:  {"avg_temp": 12, "avg_humidity": 69, "avg_rain_days": 9,  "description": "Mild"},
        5:  {"avg_temp": 17, "avg_humidity": 68, "avg_rain_days": 11, "description": "Warm"},
        6:  {"avg_temp": 21, "avg_humidity": 68, "avg_rain_days": 12, "description": "Warm"},
        7:  {"avg_temp": 23, "avg_humidity": 67, "avg_rain_days": 11, "description": "Warm and sunny"},
        8:  {"avg_temp": 22, "avg_humidity": 68, "avg_rain_days": 10, "description": "Warm and sunny"},
        9:  {"avg_temp": 17, "avg_humidity": 72, "avg_rain_days": 8,  "description": "Mild"},
        10: {"avg_temp": 11, "avg_humidity": 78, "avg_rain_days": 9,  "description": "Cool"},
        11: {"avg_temp": 5,  "avg_humidity": 83, "avg_rain_days": 10, "description": "Cold"},
        12: {"avg_temp": 0,  "avg_humidity": 85, "avg_rain_days": 11, "description": "Cold and snowy"},
    },
}


def seed_airports():
    """Seeds the airports table."""
    conn = get_connection()
    print("\nSeeding airports...")
    try:
        with conn.cursor() as cur:
            for airport in AIRPORTS:
                cur.execute("""
                    INSERT INTO airports (name, iata_code, city, region)
                    VALUES (%(name)s, %(iata_code)s, %(city)s, %(region)s)
                    ON CONFLICT (iata_code) DO NOTHING
                """, airport)
                print(f"  ✅ {airport['name']} ({airport['iata_code']})")
        conn.commit()
    finally:
        conn.close()
    print("Airports seeded successfully.")


def seed_climate_data():
    """Seeds monthly climate averages for all destinations."""
    conn = get_connection()
    print("\nSeeding climate data...")
    try:
        with conn.cursor() as cur:
            for city, months in CLIMATE_DATA.items():
                cur.execute(
                    "SELECT id FROM destinations WHERE name = %s", (city,)
                )
                row = cur.fetchone()
                if not row:
                    print(f"  ⚠️  {city} not found — skipped")
                    continue
                destination_id = row[0]
                for month, data in months.items():
                    cur.execute(
                        """
                        INSERT INTO climate_data (
                            destination_id, month,
                            avg_temp, avg_humidity,
                            avg_rain_days, description
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (destination_id, month)
                        DO UPDATE SET
                            avg_temp      = EXCLUDED.avg_temp,
                            avg_humidity  = EXCLUDED.avg_humidity,
                            avg_rain_days = EXCLUDED.avg_rain_days,
                            description   = EXCLUDED.description
                    """, (
                        destination_id, month,
                        data["avg_temp"], data["avg_humidity"],
                        data["avg_rain_days"], data["description"]
                    ))
                print(f"  ✅ {city} — 12 months seeded")
        conn.commit()
    finally:
        conn.close()
    print("Climate data seeded successfully.")


def seed():
    """
    Seeds the database with all destinations, cost data,
    airports and climate data.
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

    seed_airports()
    seed_climate_data()
    print("\nDone! Database seeded successfully.")


if __name__ == "__main__":
    seed()