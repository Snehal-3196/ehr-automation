from playwright.sync_api import sync_playwright
import time

def go_to_connection_and_edit(connection_name="EpicStandaloneConnection"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()

        try:
            # LOGIN
            page.goto("https://demo.ehrconnect.healthconnect.systems/login")
            page.wait_for_load_state("networkidle")
            page.fill("#username", "administrator")
            page.fill("#password", "Mindbowser@123")
            try:
                page.click("button[type='submit']")
            except:
                page.click("button")
            page.wait_for_timeout(3000)

            # GO TO CONNECTIONS PAGE
            try:
                page.click("text=Connections")
            except:
                page.click("a:has-text('Connections')")
            page.wait_for_timeout(2000)

            # CLICK MANAGE ON NEWLY ADDED CONNECTION
            manage_clicked = False
            try:
                page.click(f"tr:has-text('{connection_name}') button:has-text('Manage')", timeout=3000)
                print(f"✅ Clicked Manage for '{connection_name}'\n")
                manage_clicked = True
            except:
                pass
            if not manage_clicked:
                try:
                    menu_btn = page.locator(f"tr:has-text('{connection_name}') button[aria-label*='menu' i]")
                    if menu_btn.count() > 0:
                        menu_btn.first.click()
                        page.wait_for_timeout(1000)
                        page.click("button:has-text('Manage')")
                        print(f"✅ Clicked Manage from menu\n")
                        manage_clicked = True
                except:
                    pass
            if not manage_clicked:
                try:
                    page.locator("button:has-text('Manage')").first.click()
                    print("✅ Clicked first Manage button\n")
                    manage_clicked = True
                except:
                    pass
            if not manage_clicked:
                print(f"⚠️ Could not find Manage button for '{connection_name}'")
                input("Press Enter after clicking Manage manually...")
            page.wait_for_timeout(2000)

            # CLICK EDIT BUTTON
            edit_selectors = [
                "button:has-text('Edit')",
                "a:has-text('Edit')",
                "[aria-label='Edit']",
                ".edit-button"
            ]
            edit_clicked = False
            for selector in edit_selectors:
                try:
                    page.locator(selector).first.click()
                    print("✅ Clicked Edit button\n")
                    edit_clicked = True
                    break
                except:
                    continue
            if not edit_clicked:
                print("⚠️ Could not find Edit button")
                input("Press Enter after clicking Edit manually...")
            page.wait_for_timeout(2000)

            print("\n✅ Script completed: Navigated to Connections, clicked Manage, and clicked Edit.")
            print(f"🔗 Current URL: {page.url}")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            page.screenshot(path="error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    go_to_connection_and_edit(connection_name="PerrylHealth")
