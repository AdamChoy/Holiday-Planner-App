from backend.weather import get_weather
import os
from dotenv import load_dotenv
load_dotenv()

# Check key is being read
print("API Key:", os.getenv("OPENWEATHER_API_KEY"))

result = get_weather("Barcelona")

print(f"City:         {result['city']}, {result['country']}")
print(f"Temperature:  {result['avg_temp']}°C (feels like {result['feels_like']}°C)")
print(f"Humidity:     {result['humidity']}%")
print(f"Cloudiness:   {result['cloudiness']}%")
print(f"Wind Speed:   {result['wind_speed']} km/h")
print(f"Description:  {result['weather_description']}")
print(f"Coordinates:  {result['lat']}, {result['lon']}")

print(f"\n5 Day Forecast:")
for day in result["forecast"]:
    print(f"  {day['date']} — {day['avg_temp']}°C — {day['description']}")