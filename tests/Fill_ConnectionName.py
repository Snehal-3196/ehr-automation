from playwright.sync_api import sync_playwright, expect

def test_add_standalone_connection():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        # -----------------------------
        # 1. LOGIN
        # -----------------------------
        page.goto("https://demo.ehrconnect.healthconnect.systems/login", wait_until="domcontentloaded")

        page.wait_for_selector("input[type='text'], input[type='email']")
        page.fill("input[type='text'], input[type='email']", "administrator")
        page.fill("input[type='password']", "Mindbowser@123")

        page.click("button:has-text('Login'), button:has-text('Sign In')")
        
        # Dashboard load
        page.wait_for_url("**/dashboard**", timeout=30000)

        # -----------------------------
        # 2. VIEW CONNECTIONS
        # -----------------------------
        page.wait_for_selector("text=View Connections", timeout=30000)
        page.click("text=View Connections")

        # Connections page
        page.wait_for_url("**/connections**", timeout=30000)

        page.wait_for_selector("text=Connections", timeout=30000)

        # -----------------------------
        # 3. ADD NEW CONNECTION
        # -----------------------------
        page.wait_for_selector("text=Add New Connection", timeout=30000)
        page.click("text=Add New Connection")

        # -----------------------------
        # 4. SELECT EPIC
        # -----------------------------
        page.wait_for_selector("text=Epic", timeout=30000)
        page.click("text=Epic")

        # -----------------------------
        # 5. SELECT STANDALONE LAUNCH
        # -----------------------------
        page.wait_for_selector("text=Standalone Launch", timeout=30000)
        page.click("text=Standalone Launch")

        # -----------------------------
        # 6. VERIFY FORM OPENED
        # -----------------------------
        page.wait_for_selector(
            "input[placeholder*='Connection'], input[name*='connection'], input[type='text']",
            timeout=30000
        )

        # -----------------------------
        # 7. FILL CONNECTION NAME
        # -----------------------------
        page.fill(
            "input[placeholder*='Connection'], input[name*='connection'], input[type='text']",
            "Epic Standalone Automation"
        )

        print("✅ Standalone Launch connection form opened and name filled")

        browser.close()

if __name__ == "__main__":
    test_add_standalone_connection()
