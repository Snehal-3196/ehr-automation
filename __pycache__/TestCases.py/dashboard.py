from playwright.sync_api import sync_playwright
import pytest
import allure

def test_dashboard_ui():
    """
    Test that the dashboard page loads and key UI elements are visible.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://demo.ehrconnect.healthconnect.systems/dashboard")
        page.wait_for_load_state("networkidle")
        # Example checks - update selectors as needed for your dashboard
        assert page.is_visible("text=Dashboard"), "Dashboard title not visible"
        assert page.is_visible("text=Connections") or page.is_visible("a:has-text('Connections')"), "Connections menu not visible"
        # Optionally check for user/profile icon, widgets, etc.
        allure.attach(page.screenshot(full_page=True), name="dashboard_ui", attachment_type=allure.attachment_type.PNG)
        browser.close()
