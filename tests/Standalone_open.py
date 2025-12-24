from playwright.sync_api import sync_playwright, expect

def test_open_standalone_launch_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        # --------------------------------------------------
        # 1. Login Page
        # --------------------------------------------------
        page.goto("https://demo.ehrconnect.healthconnect.systems/login", timeout=60000)

        expect(page.locator("input[name='username']")).to_be_visible()
        expect(page.locator("input[name='password']")).to_be_visible()

        page.fill("input[name='username']", "administrator")
        page.fill("input[name='password']", "Mindbowser@123")

        page.click("button[type='submit']")

        # --------------------------------------------------
        # 2. Dashboard
        # --------------------------------------------------
        expect(page.locator("text=View Connections")).to_be_visible(timeout=30000)

        # --------------------------------------------------
        # 3. Go to Connections Page
        # --------------------------------------------------
        page.click("text=View Connections")

        expect(
            page.locator("h1, h2").filter(has_text="Connections")
        ).to_be_visible(timeout=30000)

        # --------------------------------------------------
        # 4. Click Add New Connection
        # --------------------------------------------------
        expect(page.locator("text=Add New Connection")).to_be_visible()
        page.click("text=Add New Connection")

        # --------------------------------------------------
        # 5. Select Epic
        # --------------------------------------------------
        epic_card = page.locator(
            "button:has-text('Epic'), div:has-text('Epic')"
        ).first

        expect(epic_card).to_be_visible(timeout=30000)
        epic_card.click()

        # --------------------------------------------------
        # 6. Select Standalone Launch (NOT Embed)
        # --------------------------------------------------
        standalone_option = page.locator(
            "text=Standalone Launch"
        )

        expect(standalone_option).to_be_visible(timeout=30000)
        standalone_option.click()

        # --------------------------------------------------
        # 7. Verify Standalone Launch Form Opened
        # --------------------------------------------------
        expect(
            page.locator(
                "form, h2, h3"
            ).filter(has_text="Standalone")
        ).to_be_visible(timeout=30000)

        print("✅ Standalone Launch form opened successfully")

        browser.close()  # keep open for debugging

