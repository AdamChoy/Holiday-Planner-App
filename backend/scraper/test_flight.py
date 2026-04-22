from backend.scraper.flights_scraper import get_cheapest_flight

result = get_cheapest_flight(
    origin_iata="LGW",
    destination_iata="BCN",
    departure_date="2026-05-01",
    return_date="2026-05-08"
)
print(result)