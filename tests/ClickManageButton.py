import pytest
from playwright.sync_api import sync_playwright

def test_07_manage_connection():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        try:
            print("=" * 70)
            print("TEST 7: MANAGE CONNECTION")
            print("=" * 70)
            # Login
            print("\n[Step 1] Login...")
            page.goto("https://demo.ehrconnect.healthconnect.systems/login")
            page.wait_for_load_state("networkidle")
            page.fill("#username", "administrator")
            page.fill("#password", "Mindbowser@123")
            try:
                page.click("button[type='submit']")
            except:
                page.click("button")
            page.wait_for_timeout(3000)
            print("✅ Logged in")
            # Navigate to Connections
            print("\n[Step 2] Navigate to Connections...")
            try:
                page.click("text=Connections")
            except:
                page.click("a:has-text('Connections')")
            page.wait_for_timeout(3000)
            print("✅ On Connections page")
            # Click Manage on first connection
            print("\n[Step 3] Clicking Manage button...")
            manage_selectors = [
                "button:has-text('Manage')",
                "a:has-text('Manage')",
                "[aria-label='Manage']"
            ]
            manage_clicked = False
            for selector in manage_selectors:
                try:
                    page.locator(selector).first.click()
                    print("✅ Manage button clicked")
                    manage_clicked = True
                    break
                except:
                    continue
            if not manage_clicked:
                print("⚠️ Please click Manage button manually on any connection")
                # For pytest, do not use input(). Just fail the test.
                pytest.fail("Could not find Manage button automatically.")
            page.wait_for_timeout(2000)
            page.screenshot(path="test_07_manage_connection.png", full_page=True)
            print("\n📸 Screenshot saved: test_07_manage_connection.png")
            print("\n" + "=" * 70)
            print("✅ TEST 7 COMPLETED")
            print("=" * 70)
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            page.screenshot(path="error.png")
            raise
        finally:
            browser.close()