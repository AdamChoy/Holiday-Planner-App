"""
driver.py
=========
Purpose: Creates and configures a Chrome browser instance that Selenium can control.
Automatically detects the installed Chrome version and downloads the matching 
ChromeDriver — so it works on any machine without manual configuration.

Usage:
    from backend.scraper.driver import get_driver

    driver = get_driver()
    driver.get("https://www.numbeo.com")
    # now scrape...
    driver.quit()
"""

import subprocess
import re
from selenium import webdriver                              # Controls Chrome
from selenium.webdriver.chrome.options import Options       # Configures Chrome behaviour
from selenium.webdriver.chrome.service import Service       # Manages ChromeDriver process
from webdriver_manager.chrome import ChromeDriverManager    # Auto-downloads correct ChromeDriver


def get_chrome_version() -> str:
    """
    Detects the installed Chrome version on the current machine.
    Works on Windows, Mac, and Linux so any teammate can run this.

    Returns:
        str: Chrome version string e.g. "147.0.7727.102"
             Returns None if Chrome version cannot be detected.
    """
    try:
        # --- Windows ---
        output = subprocess.check_output(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
            shell=True
        ).decode()
        version = output.strip().split()[-1]
        print(f"[Driver] Chrome version detected: {version}")
        return version

    except Exception:
        try:
            # --- Mac ---
            output = subprocess.check_output(
                ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
            ).decode()
            version = re.search(r"[\d.]+", output).group()
            print(f"[Driver] Chrome version detected: {version}")
            return version

        except Exception:
            try:
                # --- Linux ---
                output = subprocess.check_output(
                    ["google-chrome", "--version"]
                ).decode()
                version = re.search(r"[\d.]+", output).group()
                print(f"[Driver] Chrome version detected: {version}")
                return version

            except Exception as e:
                print(f"[Driver] Could not detect Chrome version: {e}")
                return None


def get_driver(headless=False):
    """
    Returns a configured Selenium Chrome WebDriver instance.
    Automatically matches ChromeDriver version to installed Chrome.

    Args:
        headless (bool): Run without browser window. Keep False while
                         developing so you can see what the browser is doing.
                         Switch to True only in production.

    Returns:
        webdriver.Chrome: Configured Chrome driver instance
    """
    options = Options()

    # --- Window & Stability Settings ---
    options.add_argument("--window-size=1920,1080")     # Standard desktop resolution
    options.add_argument("--no-sandbox")                # Prevents Chrome from crashing
    options.add_argument("--disable-dev-shm-usage")     # Prevents Chrome from crashing

    # --- Bot Disguise Settings ---
    # By default Selenium broadcasts that it's a bot — these lines hide that
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    # --- Headless Mode ---
    # Runs Chrome invisibly with no window — switch to True after deployment
    if headless:
        options.add_argument("--headless=new")

    # --- Auto detect Chrome version and download matching ChromeDriver ---
    chrome_version = get_chrome_version()

    if chrome_version:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(driver_version=chrome_version).install()),
            options=options
        )
    else:
        # Fallback — let webdriver_manager pick the best available version
        print("[Driver] Falling back to default ChromeDriver version")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    # --- Final Bot Detection Bypass ---
    # Hides the navigator.webdriver JavaScript property that reveals automation
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


if __name__ == "__main__":
    driver = get_driver(headless=False)
    driver.get("https://www.google.com")
    print("Page title:", driver.title)
    driver.quit()