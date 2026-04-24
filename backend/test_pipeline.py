"""
test_pipeline.py
----------------
Tests the full backend pipeline end to end.
Simulates a user searching for a holiday.
"""

from backend.database.db import get_all_destinations, get_airports
from backend.recommender import get_recommendations

# ================================================================
# Simulate user inputs from the frontend form
# ================================================================
user_inputs = {
    "budget":             600,
    "departure_date":     "2026-05-01",
    "return_date":        "2026-05-08",
    "num_people":         4,
    "vibes":              ["nightlife"],
    "weather_preference": "cold",
    "origin_airport":     "LGW"
}

print("=" * 50)
print("Holiday Planner — Backend Pipeline Test")
print("=" * 50)
print(f"\nUser Inputs:")
print(f"  Budget:       £{user_inputs['budget']}")
print(f"  Dates:        {user_inputs['departure_date']} → {user_inputs['return_date']}")
print(f"  People:       {user_inputs['num_people']}")
print(f"  Vibes:        {user_inputs['vibes']}")
print(f"  Weather:      {user_inputs['weather_preference']}")
print(f"  Airport:      {user_inputs['origin_airport']}")

# ================================================================
# Step 1 — Load destinations from database
# ================================================================
print("\n[Step 1] Loading destinations from database...")
destinations = get_all_destinations()
print(f"  Found {len(destinations)} destinations")

# ================================================================
# Step 2 — Load airports from database
# ================================================================
print("\n[Step 2] Loading airports from database...")
airports = get_airports()
print(f"  Found {len(airports)} airports")

# ================================================================
# Step 3 — Run recommender
# ================================================================
print("\n[Step 3] Scoring destinations...")
print("  (This may take a minute — fetching live flight and hotel data)\n")

results = get_recommendations(
    destinations=destinations,
    user_inputs=user_inputs,
    top_n=5
)

# ================================================================
# Step 4 — Print results
# ================================================================
print("\n" + "=" * 50)
print("🏆 Top 5 Recommended Destinations")
print("=" * 50)

for i, dest in enumerate(results, 1):
    print(f"\n{i}. {dest['name']}, {dest['country']}")
    print(f"   Final Score:    {dest['final_score']}/10")
    print(f"   Vibe Score:     {dest['vibe_score']}/10")
    print(f"   Budget Score:   {dest['budget_score']}/10")
    print(f"   Weather Score:  {dest['weather_score']}/10")
    print(f"   Safety Score:   {dest['safety_score']}/10")
    print(f"   ─────────────────────────")
    print(f"   ✈️  Flight:      £{dest.get('flight_cost', 'N/A')}")
    print(f"   🏨  Hotel/night: £{dest.get('avg_hotel_per_night', 'N/A')}")
    print(f"   🍽️  Meal cost:   £{dest.get('avg_meal_cost', 'N/A')}")
    print(f"   💰  Total cost:  £{dest.get('total_cost', 'N/A')}")
    print(f"   🌡️  Temp:        {dest.get('avg_temp', 'N/A')}°C — {dest.get('weather_description', '')}")
    print(f"   ⚠️  Over budget: {dest.get('is_over_budget', False)}")