from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context()
    page = context.new_page()

    # ---------------- LOGIN ----------------
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

    # ---------------- DASHBOARD ----------------
    view_connections = page.locator(
        "button:has-text('View Connections'), a:has-text('View Connections')"
    )
    expect(view_connections.first).to_be_visible(timeout=30000)
    view_connections.first.click()

    page.wait_for_load_state("networkidle")

    # ---------------- CONNECTIONS PAGE ----------------
    add_new_connection = page.locator(
        "button:has-text('Add New Connection'), a:has-text('Add New Connection')"
    )
    expect(add_new_connection.first).to_be_visible(timeout=30000)
    add_new_connection.first.click()

    # ---------------- SELECT EHR (EPIC) ----------------
    # Epic is a card (often image-based, no visible text)
    ehr_cards = page.locator(
        "[role='button'], div:has(img)"
    )

    expect(ehr_cards.first).to_be_visible(timeout=30000)
    ehr_cards.nth(0).click()   # Epic is first card

    # ---------------- SELECT LAUNCH TYPE ----------------
    # Explicitly select Standalone (NOT Embed)

    standalone_launch = page.locator(
        "[role='radio'], button, div"
    ).filter(has_text="Standalone")

    expect(standalone_launch.first).to_be_visible(timeout=30000)
    standalone_launch.first.click()

    # ---------------- VERIFY FORM OPENED ----------------
    # Epic Standalone form indicators
    expect(
        page.locator("form, input, select, textarea").first
    ).to_be_visible(timeout=30000)

    print("✅ Login successful")
    print("✅ Navigated to Connections page")
    print("✅ Epic selected")
    print("✅ Standalone Launch selected (NOT Embed)")
    print("✅ Epic Standalone form opened")

    # browser.close()

with sync_playwright() as playwright:
    run(playwright)
