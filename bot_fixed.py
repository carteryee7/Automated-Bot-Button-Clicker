from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import sys
import time

# NOTE: Ensure chromedriver is installed and on your PATH, or use a webdriver manager.
# This script demonstrates the fixes: correct imports, WebDriverWait usage, CSS selector for multiple
# classes (use '.' between classes), and basic error handling.

def main():
    # 1. Open the browser
    options = Options()
    driver = None
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    # Detect common Chromium/Chrome binary locations
    possible_bins = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    binary = None
    for b in possible_bins:
        if os.path.exists(b):
            options.binary_location = b
            binary = b
            break

    if not binary:
        print("Error: No Chromium/Chrome binary found in the container. Install Chromium/Chrome and try again.")
        print("On Debian/Ubuntu: sudo apt-get update && sudo apt-get install -y chromium chromium-driver")
        sys.exit(1)

    service = Service(ChromeDriverManager().install(), log_path="chromedriver.log")
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print("Failed to start ChromeDriver/Chrome:", e)
        if os.path.exists("chromedriver.log"):
            print("\n--- Chromedriver log start ---\n")
            print(open("chromedriver.log", "r", encoding="utf-8", errors="replace").read())
            print("\n--- Chromedriver log end ---\n")
        raise

    try:
        # 2. Go to the website
        driver.get("https://www.chess.com/")

        # Use an explicit wait for the element to be clickable
        wait = WebDriverWait(driver, 10)
        css_selector = (
            ".cc-button-component.cc-button-primary.cc-bg-primary"
            ".cc-button-full.landing-page-button.landing-page-hero-button"
            ".cc-button-x-large"
        )

        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        button.click()

        # optional: give the page a moment to react
        time.sleep(2)

    except TimeoutException:
        print("Timed out waiting for the button to appear/click.")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
