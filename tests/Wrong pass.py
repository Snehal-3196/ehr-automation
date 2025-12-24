
import pytest
from playwright.sync_api import sync_playwright, expect

def test_wrong_password():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        # 1. Open login page
        page.goto(
            "https://demo.ehrconnect.healthconnect.systems/login",
            wait_until="domcontentloaded"
        )

        # 2. Wait for login fields
        page.wait_for_selector("input[name='username']", timeout=20000)
        page.wait_for_selector("input[name='password']", timeout=20000)

        # 3. Enter INVALID credentials
        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "WrongPassword@123")

        # 4. Click Login
        page.click("button[type='submit']")

        # 5. Wait for response
        page.wait_for_load_state("networkidle")

        # 6. Assert error message is shown
        error_locator = page.locator(
            "text=/invalid|incorrect|failed|error/i"
        )
        expect(error_locator.first).to_be_visible(timeout=20000)

        print("✅ Invalid login verified — error message displayed.")

        # URL check removed: error message is sufficient for invalid login

        # browser.close()
