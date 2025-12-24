from playwright.sync_api import sync_playwright
import pytest
import allure

def test_login_page_ui():
    """
    Test that the login page loads and key UI elements are visible, and that username and password fields can be filled.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demo.ehrconnect.healthconnect.systems/login")
        page.wait_for_load_state("networkidle")
        # Check for username field
        assert page.is_visible("#username"), "Username field not visible"
        # Fill username
        page.fill("#username", "administrator")
        # Check for password field
        assert page.is_visible("#password"), "Password field not visible"
        # Fill password
        page.fill("#password", "Mindbowser@123")
        # Check for login button
        assert page.is_visible("button[type='submit']") or page.is_visible("button:has-text('Sign In')"), "Login button not visible"
        # Optionally, check for page title or logo
        assert "login" in page.url.lower(), "Not on login page"
        allure.attach(page.screenshot(full_page=True), name="login_page_ui", attachment_type=allure.attachment_type.PNG)
        browser.close()
