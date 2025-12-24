
import pytest
from playwright.sync_api import sync_playwright, expect

def test_dashboard_ui():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        # ---------- LOGIN ----------
        page.goto(
            "https://demo.ehrconnect.healthconnect.systems/login",
            wait_until="domcontentloaded"
        )

        page.wait_for_selector("input[name='username']", timeout=20000)
        page.wait_for_selector("input[name='password']", timeout=20000)

        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "Mindbowser@123")

        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # ---------- DASHBOARD VALIDATION ----------

        # Confirm not on login page
        expect(page).not_to_have_url(r".*/login.*")

        # Wait for sidebar (stable anchor)
        page.wait_for_selector("nav, aside", timeout=30000)

        # Wait specifically for View Connections (strong signal dashboard loaded)
        view_connections = page.locator(
            "button:has-text('View Connections'), a:has-text('View Connections')"
        )
        expect(view_connections.first).to_be_visible(timeout=30000)

        print("✅ Dashboard loaded")
        print("✅ View Connections button visible")
        browser.close()
