"""
numbeo_scraper.py
=================
Purpose: Scrapes cost of living and safety data from Numbeo.com for a given city.
Prices are forced to GBP via URL parameter so no currency conversion is needed.
Returns four key fields used in the destination dictionary:
    - avg_meal_cost_gbp: Cost of a cheap restaurant meal in GBP
    - safety_index: Safety score out of 100 (higher = safer)
    - crime_index: Crime score out of 100 (lower = safer)
    - cost_of_living_index: Overall cost score (lower = cheaper)

Usage:
    from backend.scraper.numbeo_scraper import scrape_numbeo
    result = scrape_numbeo("Bangkok")
"""

import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from backend.scraper.driver import get_driver


def scrape_numbeo(city: str, country: str) -> dict:
    """
    Scrapes cost of living and safety data from Numbeo for a given city.
    Forces GBP display via URL parameter.

    Args:
        city (str): City name e.g. "Bangkok", "Bali", "Cancun"

    Returns:
        dict: {
            "city": str,
            "avg_meal_cost_gbp": float or None,
            "safety_index": float or None,
            "crime_index": float or None,
            "cost_of_living_index": float or None
        }
    """
    driver = get_driver(headless=False)  # Keep False while testing

    results = {
        "city": city,
        "avg_meal_cost_gbp": None,
        "safety_index": None,
        "crime_index": None,
        "cost_of_living_index": None,
    }

    try:
        # --- Step 1: Format city name for URL ---
        # e.g. "Ho Chi Minh City" → "Ho-Chi-Minh-City"
        city_slug = city.strip().replace(" ", "-")

        # --- Step 2: Scrape meal cost ---
        # ?displayCurrency=GBP forces Numbeo to show all prices in GBP
        url = f"https://www.numbeo.com/cost-of-living/in/{city_slug}?displayCurrency=GBP"
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)

                if "Meal at an Inexpensive Restaurant" in label:
                    clean = value.replace("£", "").replace(",", "").strip().split()[0]
                    try:
                        results["avg_meal_cost_gbp"] = float(clean)
                    except ValueError:
                        pass

        # --- Step 3: Scrape safety and crime indices from crime page ---
        safety_url = f"https://www.numbeo.com/crime/in/{city_slug}"
        driver.get(safety_url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        index_rows = soup.find_all("tr")

        for row in index_rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)

                if "Safety Index" in label:
                    try:
                        results["safety_index"] = float(value)
                    except ValueError:
                        pass

                if "Crime Index" in label:
                    try:
                        results["crime_index"] = float(value)
                    except ValueError:
                        pass

        # --- Step 4: Scrape cost of living index from comparison page ---
        # Comparing against London gives a reliable relative cost of living index
        compare_url = (
            f"https://www.numbeo.com/cost-of-living/compare_cities.jsp"
            f"?country1=United+Kingdom&city1=London"
            f"&country2={country.replace(' ', '+')}&city2={city_slug}"
        )
        driver.get(compare_url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        all_rows = soup.find_all("tr")

        for row in all_rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)

                # Cost of living index appears as the city name with a score
                # e.g. 'Bangkok' | '41.72'
                if label.lower() == city.lower():
                    try:
                        results["cost_of_living_index"] = float(value)
                    except ValueError:
                        pass

    except Exception as e:
        try:
            driver.save_screenshot("numbeo_error.png")
            print("[Numbeo] Error screenshot saved as numbeo_error.png")
        except:
            pass
        print(f"[Numbeo] Error type: {type(e).__name__}")
        print(f"[Numbeo] Error message: {str(e)[:200]}")

    finally:
        driver.quit()

    return results

# Test
if __name__ == "__main__":
    result = scrape_numbeo("Bangkok", "Thailand")
    print(result)