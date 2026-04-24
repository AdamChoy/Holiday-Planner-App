from backend.weather import get_weather, get_weather_band

# Test 1 — live weather (within 5 days)
print("=== Live Weather ===")
result = get_weather("Barcelona")
print(f"City:         {result['city']}")
print(f"Temperature:  {result['avg_temp']}°C")
print(f"Band:         {result['weather_band']}")
print(f"Humidity:     {result['humidity']}%")
print(f"Description:  {result['weather_description']}")
print(f"Source:       {result['source']}")

print(f"\n5 Day Forecast:")
for day in result["forecast"]:
    print(f"  {day['date']} — {day['avg_temp']}°C — {day['description']}")

# Test 2 — historical weather (future trip)
print("\n=== Historical Weather (August trip) ===")
result2 = get_weather(
    city="Barcelona",
    travel_date="2026-08-15",
    destination_id=1
)
print(f"City:         {result2['city']}")
print(f"Temperature:  {result2['avg_temp']}°C")
print(f"Band:         {result2['weather_band']}")
print(f"Humidity:     {result2['humidity']}%")
print(f"Description:  {result2['weather_description']}")
print(f"Source:       {result2['source']}")

# Test 3 — weather band function
print("\n=== Weather Band Tests ===")
print(f"10°C -> {get_weather_band(10)}")   # cool
print(f"20°C -> {get_weather_band(20)}")   # warm
print(f"30°C -> {get_weather_band(30)}")   # hot