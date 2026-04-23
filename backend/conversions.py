"""
conversion.py
-------------
Handles all currency conversions to GBP.
Uses fixed yearly average exchange rates for consistency.
Rates are reviewed and updated annually.

Usage:
    from backend.conversion import convert_to_gbp, parse_price_to_gbp
"""

# -------------------------------------------------------------------
# Fixed yearly average exchange rates to GBP
# Source: Bank of England / XE.com yearly averages
# Last updated: 2026
# -------------------------------------------------------------------
YEARLY_RATES = {
    "EUR": 0.84,   # Eurozone
    "USD": 0.78,   # US Dollar
    "GBP": 1.0,    # UK — no conversion needed
    "CHF": 0.88,   # Switzerland
    "NOK": 0.070,  # Norway
    "SEK": 0.072,  # Sweden
    "DKK": 0.11,   # Denmark
    "ISK": 0.0054, # Iceland
    "HUF": 0.0021, # Hungary
    "PLN": 0.19,   # Poland
    "CZK": 0.033,  # Czech Republic
    "RON": 0.17,   # Romania
    "BGN": 0.43,   # Bulgaria
    "RSD": 0.0071, # Serbia
    "BAM": 0.43,   # Bosnia
    "MKD": 0.014,  # North Macedonia
    "ALL": 0.0082, # Albania
    "MDL": 0.042,  # Moldova
}

# -------------------------------------------------------------------
# Currency symbol to code mapping
# -------------------------------------------------------------------
SYMBOL_TO_CODE = {
    "€":   "EUR",
    "$":   "USD",
    "£":   "GBP",
    "Fr":  "CHF",
    "Ft":  "HUF",
    "zł":  "PLN",
    "Kč":  "CZK",
    "lei": "RON",
    "лв":  "BGN",
    "kr":  "NOK",  # Default — resolved by country below
}

# -------------------------------------------------------------------
# kr is shared by Norway, Sweden, Denmark and Iceland
# Resolved by passing country name to parse_price_to_gbp
# -------------------------------------------------------------------
KR_CURRENCY_BY_COUNTRY = {
    "Norway":  "NOK",
    "Sweden":  "SEK",
    "Denmark": "DKK",
    "Iceland": "ISK",
}


def convert_to_gbp(amount: float, from_currency: str) -> float:
    """
    Converts a numeric amount to GBP using fixed yearly rates.

    Args:
        amount:        Numeric amount to convert
        from_currency: Currency code e.g. "EUR", "NOK"

    Returns:
        Amount in GBP rounded to 2 decimal places
    """
    if amount is None:
        return None

    rate = YEARLY_RATES.get(from_currency, 1.0)
    return round(amount * rate, 2)


def parse_price_to_gbp(
    price_string: str,
    currency_code: str = None,
    country: str = None
) -> dict:
    """
    Parses a price string from SerpAPI and converts to GBP.
    Uses fixed yearly rates for consistency.
    Returns a single clean price not a range.

    Args:
        price_string:  Raw price string e.g. "€20–30", "$$", "€100"
        currency_code: Override currency code e.g. "CZK"
        country:       Country name to resolve kr currency
                       e.g. "Norway" -> NOK, "Sweden" -> SEK

    Returns:
        dict:
            price   - price in GBP (float or None)
            display - clean display string e.g. "£17"

    """
    if not price_string or price_string in ("N/A", ""):
        return {"price": None, "display": "N/A"}

    # --- Dollar sign levels e.g. "$", "$$", "$$$" ---
    if set(price_string).issubset({"$"}):
        levels = {"$": 10, "$$": 25, "$$$": 60, "$$$$": 120}
        amount = levels.get(price_string, 25)
        gbp = convert_to_gbp(amount, "USD")
        return {"price": gbp, "display": f"~£{round(gbp)}"}

    # --- Determine currency ---
    if currency_code:
        currency = currency_code
        for symbol in SYMBOL_TO_CODE:
            price_string = price_string.replace(symbol, "").strip()
    else:
        currency = "EUR"
        if "kr" in price_string:
            currency = KR_CURRENCY_BY_COUNTRY.get(country, "NOK")
            price_string = price_string.replace("kr", "").strip()
        else:
            for symbol, code in SYMBOL_TO_CODE.items():
                if symbol in price_string:
                    currency = code
                    price_string = price_string.replace(symbol, "").strip()
                    break

    # --- Take only first value from a range e.g. "20–30" -> "20" ---
    for separator in ["–", "-"]:
        if separator in price_string:
            price_string = price_string.split(separator)[0].strip()
            break

    # --- Convert to GBP ---
    try:
        amount = float(price_string.replace("+", "").strip())
        gbp = convert_to_gbp(amount, currency)
        return {"price": gbp, "display": f"£{round(gbp)}"}
    except ValueError:
        pass

    return {"price": None, "display": price_string}