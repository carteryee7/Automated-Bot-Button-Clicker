"""Robust chess.com button clicker

Usage examples:
  python bot.py                       # tries cookie accept button automatically
  python bot.py --selector-type css --selector ".cc-button-component.cc-button-primary"  # custom CSS selector
  python bot.py --headless            # run headless (no UI)

This script uses webdriver-manager to install a matching chromedriver and supports multiple selector types
(css, xpath, text). It tries a few sensible defaults for cookie consent buttons on chess.com.
"""

import argparse
import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


DEFAULT_URL = "https://www.chess.com/"

# A set of fallback selectors that commonly match cookie/consent buttons on chess.com
FALLBACK_SELECTORS = [
    (By.CSS_SELECTOR, ".cc-button-component.cc-button-primary"),
    (By.CSS_SELECTOR, ".cc-button-component.cc-button-accept"),
    (By.XPATH, "//button[contains(., 'Accept') or contains(., 'Accept All') or contains(., 'I Accept')]") ,
    (By.XPATH, "//button[contains(translate(., 'ACCEPT','accept'), 'accept')]")
]


def find_and_click(driver, locators, timeout=10, poll_frequency=0.5):
    wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)
    last_err = None
    for by, selector in locators:
        try:
            # Wait for element to be clickable
            el = wait.until(EC.element_to_be_clickable((by, selector)))
            print(f"Found target using {by} selector: {selector}")
            el.click()
            return True
        except TimeoutException as e:
            last_err = e
        except Exception as e:
            last_err = e
    # If we reach here, no selector matched
    print("Failed to find a clickable element with the provided selectors.")
    if last_err:
        print("Last error:", last_err)
    return False


def build_locators(args):
    if args.selector and args.selector_type:
        if args.selector_type.lower() == "css":
            return [(By.CSS_SELECTOR, args.selector)]
        elif args.selector_type.lower() == "xpath":
            return [(By.XPATH, args.selector)]
        elif args.selector_type.lower() == "text":
            # Search for a button containing text
            xpath = f"//button[contains(normalize-space(.), '{args.selector}')]"
            return [(By.XPATH, xpath)]
        else:
            raise ValueError("Unknown selector type. Use css, xpath, or text.")

    # No selector provided: use fallbacks
    return FALLBACK_SELECTORS


def get_chrome_options(headless=False):
    options = Options()
    if headless:
        # Use the modern headless mode
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # If a Chrome/Chromium binary exists in common paths, set it
    possible_bins = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/snap/bin/chromium",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    for b in possible_bins:
        if os.path.exists(b):
            options.binary_location = b
            break

    return options


def main():
    parser = argparse.ArgumentParser(description="Click a button on chess.com (e.g., cookie consent)")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL to open (default: chess.com)")
    parser.add_argument("--selector-type", choices=["css", "xpath", "text"], help="Type of selector when using --selector")
    parser.add_argument("--selector", help="The selector to locate the button (CSS/XPath/text)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds to wait for the button")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")
    args = parser.parse_args()

    locators = build_locators(args)

    # Install or find chromedriver using webdriver-manager
    try:
        service = Service(ChromeDriverManager().install())
    except Exception as e:
        print("Failed to install or find ChromeDriver:", e)
        print("If you're in a container, make sure Chrome/Chromium is installed or run the provided install script.")
        sys.exit(2)

    options = get_chrome_options(headless=args.headless)

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        print("Failed to start ChromeDriver/Chrome:", e)
        sys.exit(3)

    try:
        driver.get(args.url)
        print(f"Opened: {args.url}")

        success = find_and_click(driver, locators, timeout=args.timeout)
        if success:
            print("Click successful.")
        else:
            print("Click failed — no matching element.")
    finally:
        try:
            time.sleep(1)
        except Exception:
            pass
        driver.quit()


if __name__ == "__main__":
    main()
