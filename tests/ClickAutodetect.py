from playwright.sync_api import sync_playwright, TimeoutError

def test_fill_epic_standalone_connection():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # --- 1. Go to login page ---
        page.goto("https://demo.ehrconnect.healthconnect.systems/login")

        # --- 2. Fill login credentials ---
        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "Mindbowser@123")
        page.click("button[type='submit']")

        # --- 3. Wait for dashboard / view connections link ---
        try:
            page.wait_for_selector("text=View Connections", timeout=30000)
        except TimeoutError:
            print("❌ Dashboard did not load or login failed.")
            return

        # --- 4. Navigate to connections ---
        page.click("text=View Connections")

        # --- 5. Wait for Connections page header ---
        try:
            page.wait_for_selector("h1:has-text('Connections')", timeout=30000)
        except TimeoutError:
            print("❌ Connections page did not load.")
            return

        # --- 6. Click Add New Connection ---
        page.click("text=Add New Connection")

        # --- 7. Select Epic ---
        page.wait_for_selector("text=Epic", timeout=30000)
        page.click("text=Epic")

        # --- 8. Select Standalone Launch ---
        page.wait_for_selector("text=Standalone Launch", timeout=30000)
        page.click("text=Standalone Launch")

        # --- 9. Fill Connection Name ---
        try:
            conn_name = page.wait_for_selector(
                "input[placeholder*='Connection'], input[name*='connection'], input[type='text']",
                timeout=30000
            )
            conn_name.fill("Epic Standalone Automation")
        except TimeoutError:
            print("❌ Connection Name field not found.")
            return

        # --- 10. Fill Client ID ---
        try:
            client_id = page.wait_for_selector(
                "input[placeholder*='Client'], input[name*='client'], input[type='text']",
                timeout=30000
            )
            client_id.fill("TestClientID123")
        except TimeoutError:
            print("❌ Client ID field not found.")
            return

        # --- 11. Fill Client Secret ---
        try:
            client_secret = page.wait_for_selector(
                "input[placeholder*='Secret'], input[name*='secret'], input[type='password']",
                timeout=30000
            )
            client_secret.fill("TestClientSecret123")
        except TimeoutError:
            print("❌ Client Secret field not found.")
            return

        # --- 12. Fill Base URL (FHIR Endpoint) with fallback selectors ---
        base_url_value = "https://r4.smarthealthit.org/"
        url_selectors = [
            "input[name='url']",
            "input[name='baseUrl']",
            "input[name='base_url']",
            "input[name='endpoint']",
            "input[name='fhirEndpoint']",
            "input[placeholder*='url' i]",
            "input[placeholder*='endpoint' i]",
            "input[placeholder*='fhir' i]"
        ]

        filled_base_url = False
        for selector in url_selectors:
            try:
                loc = page.locator(selector)
                if loc.count() > 0:
                    loc.first.fill(base_url_value)
                    print(f"✅ Filled Base URL: {base_url_value}")
                    filled_base_url = True
                    break
            except Exception:
                continue

        if not filled_base_url:
            print("⚠️ Could not find Base URL input.")
        
        # slight pause after filling URL
        page.wait_for_timeout(1000)

        # --- 13. Click Auto-detect ---
        try:
            auto_btn = page.wait_for_selector("button:has-text('Auto-detect')", timeout=20000)
            auto_btn.click()
            print("✅ Auto-detect clicked.")
        except TimeoutError:
            print("⚠️ Auto-detect button not found.")

        print("✅ Form filled (without submit). Browser remains open for inspection.")

        # Leave browser open for review
        # browser.close()

if __name__ == "__main__":
    test_fill_epic_standalone_connection()
