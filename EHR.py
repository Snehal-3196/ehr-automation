from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def click_with_fallbacks(page, selectors, action_name, timeout=2000):
    """
    Try a list of selectors in order and click the first one that matches.
    Returns True if a click succeeded, False otherwise.
    """
    for selector in selectors:
        try:
            page.click(selector, timeout=timeout)
            print(f"✅ {action_name} (selector: {selector})")
            return True
        except Exception as e:
            continue
    print(f"⚠️  {action_name} - no matching selector found")
    return False

def fill_input_with_fallbacks(page, selectors, value, field_name, timeout=2000):
    """
    Try a list of selectors in order and fill the first one that matches.
    Returns True if fill succeeded, False otherwise.
    """
    for selector in selectors:
        try:
            if page.locator(selector).count() > 0:
                page.fill(selector, value)
                print(f"✅ Filled {field_name}")
                return True
        except Exception as e:
            continue
    print(f"⚠️  Could not fill {field_name}")
    return False

def take_screenshot(page, step_name):
    """Take a screenshot and save with timestamp and step name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{step_name}_{timestamp}.png"
    try:
        page.screenshot(path=filename, full_page=True)
        print(f"📸 Screenshot: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️  Could not take screenshot: {e}")
        return None

def add_new_connection():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()

        try:
            # Step 1: Login
            print("=" * 60)
            print("Step 1: Logging in...")
            print("=" * 60)
            page.goto("https://demo.ehrconnect.healthconnect.systems/login")
            page.wait_for_load_state("networkidle")

            page.fill("#username", "administrator")
            page.fill("#password", "Mindbowser@123")

            try:
                page.click("button[type='submit']")
            except:
                try:
                    page.click("button:has-text('Sign In')")
                except:
                    page.click("button")

            page.wait_for_timeout(3000)
            print("✅ Logged in successfully\n")
            take_screenshot(page, "01_login")

            # Step 2: Navigate to Connections
            print("=" * 60)
            print("Step 2: Navigating to Connections...")
            print("=" * 60)
            try:
                page.click("text=Connections")
                page.wait_for_timeout(2000)
                print("✅ Opened Connections page\n")
            except:
                try:
                    page.click("a:has-text('Connections')")
                    page.wait_for_timeout(2000)
                    print("✅ Opened Connections page\n")
                except:
                    print("❌ Could not find Connections page\n")
                    take_screenshot(page, "02_connections_error")
                    return
            take_screenshot(page, "02_connections")

            # Step 3: Click Add New Connection
            print("=" * 60)
            print("Step 3: Clicking Add New Connection...")
            print("=" * 60)
            add_selectors = [
                "button:has-text('Add Connection')",
                "button:has-text('New Connection')",
                "button:has-text('Add New')",
                "button:has-text('Add')",
                "button:has-text('Create')"
            ]
            
            if click_with_fallbacks(page, add_selectors, "Clicked Add Connection button"):
                page.wait_for_timeout(2000)
                print()
                take_screenshot(page, "03_add_connection")
            else:
                print("❌ Could not find Add Connection button\n")
                take_screenshot(page, "03_add_connection_error")
                return

            # Step 4: Select Epic
            print("=" * 60)
            print("Step 4: Selecting Epic EHR...")
            print("=" * 60)
            epic_selectors = [
                "text=Epic",
                "label:has-text('Epic')",
                "input[value='Epic']",
                "[data-value='Epic']",
                "option:has-text('Epic')",
                "div:has-text('Epic')",
                "span:has-text('Epic')"
            ]
            
            click_with_fallbacks(page, epic_selectors, "Selected Epic")
            page.wait_for_timeout(2000)
            print()
            take_screenshot(page, "04_select_epic")

            # Step 5: Select Standalone
            print("=" * 60)
            print("Step 5: Selecting Standalone...")
            print("=" * 60)
            standalone_selectors = [
                "text=Standalone",
                "label:has-text('Standalone')",
                "input[value='Standalone']",
                "[data-value='Standalone']",
                "option:has-text('Standalone')",
                "div:has-text('Standalone')",
                "span:has-text('Standalone')"
            ]
            
            click_with_fallbacks(page, standalone_selectors, "Selected Standalone")
            page.wait_for_timeout(2000)
            print()
            take_screenshot(page, "05_select_standalone")

            # Step 6: Click Standalone Launch
            print("=" * 60)
            print("Step 6: Clicking Standalone Launch...")
            print("=" * 60)
            launch_selectors = [
                "button:has-text('Standalone Launch')",
                "button:has-text('Launch')",
                "button:has-text('Start')",
                "button:has-text('Continue')",
                "a:has-text('Standalone Launch')",
                "a:has-text('Launch')"
            ]
            
            click_with_fallbacks(page, launch_selectors, "Clicked Standalone Launch")
            
            # Wait and handle potential page navigation
            try:
                page.wait_for_timeout(2000)
            except:
                print("⚠️  Page may have navigated or closed")
            
            print()
            
            # Only try to take screenshot if browser is still open
            try:
                take_screenshot(page, "06_standalone_launch")
            except:
                print("⚠️  Could not take screenshot (browser may have closed)")
                # Don't return; continue to see if the form is still accessible
            
            page.wait_for_timeout(1000)

            # Step 7: Fill Connection Details
            print("=" * 60)
            print("Step 7: Filling Connection Details...")
            print("=" * 60)
            
            # Connection Name
            fill_input_with_fallbacks(page, 
                ["input[name='name']", "input[name='connectionName']", "input[placeholder*='name' i]"],
                "Epic Test Connection", "Connection Name")

            page.wait_for_timeout(1000)

            # URL/Endpoint
            fill_input_with_fallbacks(page,
                ["input[name='url']", "input[name='endpoint']", "input[placeholder*='url' i]"],
                "https://fhir.epic.com/interconnect-fhir-oauth", "URL/Endpoint")

            page.wait_for_timeout(1000)


            # Client ID
            fill_input_with_fallbacks(page,
                ["input[name='clientId']", "input[placeholder*='client' i]"],
                "test-client-id-123", "Client ID")

            page.wait_for_timeout(1000)

            # Embedded App URL
            fill_input_with_fallbacks(page,
                ["input[name='embeddedAppUrl']", "input[name='appUrl']", 
                 "input[placeholder*='embedded' i]", "input[placeholder*='app url' i]"],
                "http://localhost:5173/integrations/add", "Embedded App URL")

            print()
            page.wait_for_timeout(2000)
            take_screenshot(page, "07_connection_details")

            # Step 8: Save Connection
            print("=" * 60)
            print("Step 8: Saving Connection...")
            print("=" * 60)
            save_selectors = [
                "button:has-text('Save')",
                "button:has-text('Submit')",
                "button:has-text('Create')",
                "button:has-text('Add')",
                "button[type='submit']"
            ]
            
            if click_with_fallbacks(page, save_selectors, "Clicked Save button"):
                page.wait_for_timeout(3000)
                print()
                take_screenshot(page, "08_save_connection")
            else:
                print("⚠️ Could not find Save button\n")
                take_screenshot(page, "08_save_connection_error")

            # Step 9: Click Back Button to Return to Connections Page
            print("=" * 60)
            print("Step 9: Clicking Back Button...")
            print("=" * 60)
            back_selectors = [
                "button:has-text('Back')",
                "a:has-text('Back')",
                "button:has-text('← Back')",
                "button:has-text('< Back')",
                "[aria-label='Back']",
                ".back-button",
                "button.btn-back"
            ]
            
            if click_with_fallbacks(page, back_selectors, "Clicked Back button"):
                page.wait_for_timeout(2000)
                print()
            else:
                print("⚠️ Could not find Back button, trying browser back\n")
                try:
                    page.go_back()
                    print("✅ Used browser back navigation\n")
                except:
                    print("❌ Could not navigate back\n")
            
            page.wait_for_timeout(2000)

            # Final Screenshot
            take_screenshot(page, "09_final_connections")
            print("=" * 60)
            print("✅ CONNECTION ADDED SUCCESSFULLY!")
            print("=" * 60)
            print(f"🔗 Current URL: {page.url}")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            take_screenshot(page, "error")

        finally:
            print("\n" + "=" * 60)
        
            browser.close()

if __name__ == "__main__":
    add_new_connection()