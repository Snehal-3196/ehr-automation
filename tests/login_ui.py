
import pytest
from playwright.sync_api import sync_playwright, expect
def test_login_ui():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. Go to the login URL
        page.goto("https://demo.ehrconnect.healthconnect.systems/login")

        # Wait for the login form to load
        page.wait_for_selector("input[type='text'], input[type='email'], input[name*='user']")

        # 2. Fill username
        page.fill("input[name='username']", "your_username_here")

        # 3. Fill password
        page.fill("input[name='password']", "your_password_here")

        # 4. Click the login button
        page.click("button[type='submit'], input[type='submit']")

        # Optional: wait for navigation or some element after login
        # page.wait_for_url("**/dashboard**")
        # expect(page.locator("text=Welcome")).to_be_visible()

        print("Login script executed — check if logged in.")
        # browser.close()
