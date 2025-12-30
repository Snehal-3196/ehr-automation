from playwright.sync_api import sync_playwright
import time

def edit_connection_name(connection_name="PerrylHealth", new_name="PerrylHealth Connect"):
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

            # CLICK MANAGE ON THE CONNECTION
            manage_clicked = False
            try:
                page.click(f"tr:has-text('{connection_name}') button:has-text('Manage')", timeout=3000)
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
                        manage_clicked = True
                except:
                    pass
            if not manage_clicked:
                try:
                    page.locator("button:has-text('Manage')").first.click()
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
                    edit_clicked = True
                    break
                except:
                    continue
            if not edit_clicked:
                print("⚠️ Could not find Edit button")
                input("Press Enter after clicking Edit manually...")
            page.wait_for_timeout(2000)

            # CHANGE CONNECTION NAME
            name_selectors = [
                "input[name='name']",
                "input[name='connectionName']",
                "input[placeholder*='name' i]",
                "input[placeholder*='connection name' i]"
            ]
            for selector in name_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(new_name)
                        print(f"✅ Changed Connection Name to: {new_name}")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)

            # SAVE CHANGES
            save_selectors = [
                "button:has-text('Save')",
                "button:has-text('Update')",
                "button:has-text('Submit')",
                "button[type='submit']"
            ]
            for selector in save_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Saved changes\n")
                    break
                except:
                    continue
            page.wait_for_timeout(2000)
            print("\n✅ Script completed: Connection name changed and saved.")
            print(f"🔗 Current URL: {page.url}")
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            page.screenshot(path="error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    edit_connection_name(connection_name="PerrylHealth", new_name="PerrylHealth Connect")
