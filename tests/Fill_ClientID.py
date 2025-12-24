from playwright.sync_api import sync_playwright, TimeoutError

def test_add_standalone_connection():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set True to run in background
        context = browser.new_context()
        page = context.new_page()

        # 1. Open login page
        page.goto("https://demo.ehrconnect.healthconnect.systems/login")

        # 2. Fill credentials
        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "Mindbowser@123")
        page.click("button[type='submit']")

        # 3. Wait for dashboard: "View Connections"
        try:
            page.wait_for_selector("text=View Connections", timeout=30000)
        except TimeoutError:
            print("Dashboard did not load. Check login credentials or network.")
            return

        # 4. Click View Connections
        page.click("text=View Connections")

        # 5. Wait for Connections page to load
        try:
            page.wait_for_selector("h1:has-text('Connections')", timeout=30000)
        except TimeoutError:
            print("Connections page did not load.")
            return

        # 6. Click Add New Connection
        page.click("text=Add New Connection")

        # 7. Wait and select Epic
        page.wait_for_selector("text=Epic", timeout=30000)
        page.click("text=Epic")

        # 8. Wait and select Standalone Launch type
        page.wait_for_selector("text=Standalone Launch", timeout=30000)
        page.click("text=Standalone Launch")

        # 9. Wait for form fields to appear
        try:
            page.wait_for_selector(
                "input[placeholder*='Connection'], input[name*='connection'], input[type='text']",
                timeout=30000
            )
        except TimeoutError:
            print("Connection form did not appear.")
            return

        # 10. Fill Connection Name (flexible selector)
        page.fill(
            "input[placeholder*='Connection'], input[name*='connection'], input[type='text']",
            "Epic Standalone Automation"
        )

        # 11. Fill Client ID using similar flexible selector
        page.fill(
            "input[placeholder*='Client'], input[name*='client'], input[type='text']",
            "TestClientID123"
        )

        print("Standalone connection form filled successfully!")

        # Keep browser open for review; uncomment to close automatically
        # browser.close()

if __name__ == "__main__":
    test_add_standalone_connection()
