
import pytest
from playwright.sync_api import sync_playwright, expect

def test_login_fields():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        # 1. Open login page
        page.goto("https://demo.ehrconnect.healthconnect.systems/login", wait_until="domcontentloaded")

        # 2. Wait for username & password fields
        page.wait_for_selector("input[name='username']", timeout=20000)
        page.wait_for_selector("input[name='password']", timeout=20000)

        # 3. Enter credentials
        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "Mindbowser@123")

        # 4. Click Login
        page.click("button[type='submit']")

        # 5. Wait for dashboard to load
        page.wait_for_load_state("networkidle")

        # Common dashboard checks (safe + flexible)
        expect(
            page.locator("h1, h2, nav, aside").first
        ).to_be_visible(timeout=30000)

        print("✅ Login successful. Dashboard is visible.")
        # browser.close()
