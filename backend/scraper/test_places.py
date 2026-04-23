from backend.scraper.places_scraper import get_all_places

results = get_all_places("Barcelona", country="Spain", max_per_category=5)

print(f"Total places found: {results['total_count']}")

print(f"\n🍽️  Restaurants ({len(results['restaurants'])}):")
for p in results["restaurants"]:
    print(f"  {p['name']} — ⭐{p['rating']} — {p['price_level']['display']} — 📍{p['lat']}, {p['lon']}")

print(f"\n📍 Tourist Spots ({len(results['tourist_spots'])}):")
for p in results["tourist_spots"]:
    print(f"  {p['name']} — ⭐{p['rating']}")

print(f"\n🎉 Bars & Nightlife ({len(results['bars_nightlife'])}):")
for p in results["bars_nightlife"]:
    print(f"  {p['name']} — ⭐{p['rating']} — {p['price_level']['display']}")