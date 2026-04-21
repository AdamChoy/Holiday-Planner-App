#  creating and configuring a Chrome browser instance that Selenium can control
#  creates a Chrome browser that looks as human as possible, ready to be pointed at any website by your scrapers — and every scraper in your project will use it like this: 
# from backend.scraper.driver import get_driver

# driver = get_driver()
# driver.get("https://www.numbeo.com")
# # now scrape...
# driver.quit()

from selenium import webdriver  # controls Chrome
from selenium.webdriver.chrome.options import Options  # Allows congifuration of the behaviour of Chrome
from selenium.webdriver.chrome.service import Service  # Manages ChromeDriver process
from webdriver_manager.chrome import ChromeDriverManager # Downloads the correct ChromeDriver version which matches your isntalled Chrome


def get_driver(headless=False):
    """
    Returns a configured Selenium Chrome WebDriver instance.

    Args:
        headless (bool): Run without browser window. Keep False while
                         developing so you can see what the browser is doing.
                         Switch to True only in production.

    Returns:
        webdriver.Chrome: Configured Chrome driver instance
    """
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    if headless:
        options.add_argument("--headless=new") # headless allows the Chrome to run invisibly with no browser window. After deployment this will be turned True so it runs in the background

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )  # lauches the browser

    # Additional bot detection bypass
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver


if __name__ == "__main__":
    driver = get_driver(headless=False)
    driver.get("https://www.google.com")
    print("Page title:", driver.title)
    driver.quit()