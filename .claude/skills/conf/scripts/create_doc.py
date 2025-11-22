from playwright.sync_api import sync_playwright
import sys

# Parameterized URL (detected or user-provided)
TARGET_URL = "http://localhost:3001"  # <-- Auto-detected or from user


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(TARGET_URL)
        print("Page loaded:", page.title())

        browser.close()


if __name__ == "__main__":
    main()
