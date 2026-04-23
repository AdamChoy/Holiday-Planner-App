from backend.scraper.hotels_scraper import get_cheapest_hotel, get_hotel_options

# Test single cheapest hotel
result = get_cheapest_hotel(
    destination="Barcelona",
    check_in_date="2026-05-01",
    check_out_date="2026-05-08"
)
print("Cheapest hotel:")
print(result)

# Test multiple options
print("\nAll options:")
options = get_hotel_options(
    destination="Barcelona",
    check_in_date="2026-05-01",
    check_out_date="2026-05-08"
)
for hotel in options:
    print(hotel)