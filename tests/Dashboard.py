
import pytest
from playwright.sync_api import sync_playwright, expect

def test_dashboard_connections():
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

        # ---------- DASHBOARD ----------
        view_connections = page.locator(
            "button:has-text('View Connections'), a:has-text('View Connections')"
        )
        expect(view_connections.first).to_be_visible(timeout=30000)
        view_connections.first.click()

        # ---------- CONNECTIONS PAGE ----------
        page.wait_for_load_state("networkidle")

        # Strongest signal Connections page is loaded
        add_connection_btn = page.locator(
            "button:has-text('Add New Connection'), a:has-text('Add New Connection')"
        )
        expect(add_connection_btn.first).to_be_visible(timeout=30000)

        print("✅ Connections page loaded successfully.")
        browser.close()
    print("✅ Add New Connection button is visible.")

