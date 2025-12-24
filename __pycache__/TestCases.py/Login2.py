from playwright.sync_api import sync_playwright
import pytest
import allure

def test_login_fields_visible():
    """
    Test that the login page UI loads and username, password fields, and login button are visible.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demo.ehrconnect.healthconnect.systems/login")
        page.wait_for_load_state("networkidle")
        # Check for username field
        assert page.is_visible("#username"), "Username field not visible"
        # Check for password field
        assert page.is_visible("#password"), "Password field not visible"
        # Check for login button
        assert page.is_visible("button[type='submit']") or page.is_visible("button:has-text('Sign In')"), "Login button not visible"
        allure.attach(page.screenshot(full_page=True), name="login_fields_ui", attachment_type=allure.attachment_type.PNG)
        browser.close()
