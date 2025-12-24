from playwright.sync_api import sync_playwright, expect

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300)
        context = browser.new_context()
        page = context.new_page()

        # Go to login page
        page.goto("https://demo.ehrconnect.healthconnect.systems/login", wait_until="domcontentloaded")

        # Login
        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "Mindbowser@123")
        page.click("button[type='submit']")
        page.wait_for_load_state("networkidle")

        # Go to Connections
        view_connections = page.locator("button:has-text('View Connections'), a:has-text('View Connections')")
        expect(view_connections.first).to_be_visible(timeout=30000)
        view_connections.first.click()
        page.wait_for_load_state("networkidle")

        # Select Epic
        epic_btn = page.locator("text=Epic", has_text="Epic")
        if not epic_btn.first.is_visible():
            epic_btn = page.locator("button:has-text('Epic'), div:has-text('Epic')")
        expect(epic_btn.first).to_be_visible(timeout=10000)
        epic_btn.first.click()

        # Select Standalone
        standalone_btn = page.locator("text=Standalone", has_text="Standalone")
        if not standalone_btn.first.is_visible():
            standalone_btn = page.locator("button:has-text('Standalone'), div:has-text('Standalone')")
        expect(standalone_btn.first).to_be_visible(timeout=10000)
        standalone_btn.first.click()
        page.wait_for_load_state("networkidle")

        print("✅ Logged in, navigated to Connections, selected Epic and Standalone.")
        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    main()
