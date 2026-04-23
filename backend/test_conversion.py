from backend.conversions import convert_to_gbp, parse_price_to_gbp

print("--- Basic Conversions ---")
print(convert_to_gbp(100, "EUR"))   # £84
print(convert_to_gbp(100, "NOK"))   # £7
print(convert_to_gbp(100, "CZK"))   # £3.30
print(convert_to_gbp(100, "GBP"))   # £100

print("\n--- Price String Parsing ---")
print(parse_price_to_gbp("€20–30"))                      # £17
print(parse_price_to_gbp("$$"))                           # ~£20
print(parse_price_to_gbp("€100"))                         # £84
print(parse_price_to_gbp("N/A"))                          # N/A
print(parse_price_to_gbp("500", "NOK"))                   # £35

print("\n--- kr Currency Resolution ---")
print(parse_price_to_gbp("kr200", country="Norway"))      # £14
print(parse_price_to_gbp("kr200", country="Sweden"))      # £14
print(parse_price_to_gbp("kr200", country="Denmark"))     # £22
print(parse_price_to_gbp("kr200", country="Iceland"))     # £1