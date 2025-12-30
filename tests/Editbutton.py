from playwright.sync_api import sync_playwright, expect

def manage_and_edit_connection(connection_name="PerrylHealth"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        try:
            # 1. Login
            page.goto("https://demo.ehrconnect.healthconnect.systems/login")
            page.fill('input[name="username"]', "administrator")
            page.fill('input[name="password"]', "Mindbowser@123")
            page.click('button[type="submit"]')
            page.wait_for_url("**/dashboard", timeout=10000)

            # 2. Go to Connections page
            page.click('a:has-text("Connections")')
            page.wait_for_url("**/connections", timeout=10000)

            # 3. Find the row for the new connection and click Manage
            row = page.locator(f'tr:has-text("{connection_name}")')
            expect(row).to_be_visible(timeout=5000)
            manage_btn = row.locator('button:has-text("Manage")')
            expect(manage_btn).to_be_visible(timeout=5000)
            manage_btn.click()

            # 4. On the manage page, click Edit
            page.wait_for_url("**/connections/manage/**", timeout=10000)
            edit_btn = page.locator('button:has-text("Edit")')
            expect(edit_btn).to_be_visible(timeout=5000)
            edit_btn.click()

            print("Successfully navigated to edit page for connection:", connection_name)
        finally:
            browser.close()

if __name__ == "__main__":
    manage_and_edit_connection()