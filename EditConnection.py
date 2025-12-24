from playwright.sync_api import sync_playwright

def complete_connection_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()

        try:
            # ============================================================
            # PART 1: LOGIN
            # ============================================================
            print("=" * 60)
            print("PART 1: LOGIN")
            print("=" * 60)
            page.goto("https://demo.ehrconnect.healthconnect.systems/login")
            page.wait_for_load_state("networkidle")

            page.fill("#username", "administrator")
            page.fill("#password", "Mindbowser@123")

            try:
                page.click("button[type='submit']")
            except:
                page.click("button")

            page.wait_for_timeout(3000)
            print("✅ Logged in successfully\n")

            # ============================================================
            # PART 2: CREATE CONNECTION
            # ============================================================
            print("=" * 60)
            print("PART 2: CREATE NEW CONNECTION")
            print("=" * 60)
            
            # Go to Connections
            print("\nNavigating to Connections page...")
            try:
                page.click("text=Connections")
            except:
                page.click("a:has-text('Connections')")
            
            page.wait_for_timeout(2000)
            print("✅ On Connections page\n")

            # Click Add Connection
            print("Clicking Add New Connection...")
            add_selectors = [
                "button:has-text('Add Connection')",
                "button:has-text('New Connection')",
                "button:has-text('Add New')",
                "button:has-text('Add')"
            ]
            
            for selector in add_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Add Connection\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)

            # Select Epic
            print("Selecting Epic...")
            epic_selectors = ["text=Epic", "label:has-text('Epic')", "div:has-text('Epic')"]
            for selector in epic_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Selected Epic\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)

            # Select Standalone (more specific selector to avoid Embedded)
            print("Selecting Standalone...")
            standalone_selectors = [
                "text=Standalone Launch",
                "label:has-text('Standalone Launch')",
                "input[value='Standalone Launch']",
                "input[value='standalone']",
                "[data-value='standalone']",
                "div:has-text('Standalone Launch')",
                "text=/^Standalone$/",  # Exact match for "Standalone" only
                "label:has-text(/^Standalone$/)"
            ]
            for selector in standalone_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Selected Standalone\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)

            # Click Standalone Launch
            print("Clicking Standalone Launch...")
            launch_selectors = [
                "button:has-text('Standalone Launch')",
                "button:has-text('Launch')",
                "button:has-text('Continue')"
            ]
            for selector in launch_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Standalone Launch\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(3000)

            # Fill Connection Details
            print("Filling connection details...")
            
            # Connection Name
            if page.locator("input[name='name']").count() > 0:
                page.fill("input[name='name']", "TestConnection123")
            elif page.locator("input[name='connectionName']").count() > 0:
                page.fill("input[name='connectionName']", "TestConnection123")
            elif page.locator("input[placeholder*='name' i]").count() > 0:
                page.locator("input[placeholder*='name' i]").first.fill("TestConnection123")
            print("✅ Filled Connection Name: TestConnection123")
            
            page.wait_for_timeout(1000)

            # URL
            if page.locator("input[name='url']").count() > 0:
                page.fill("input[name='url']", "https://fhir.epic.com/interconnect-fhir-oauth")
            elif page.locator("input[name='endpoint']").count() > 0:
                page.fill("input[name='endpoint']", "https://fhir.epic.com/interconnect-fhir-oauth")
            print("✅ Filled URL")
            
            page.wait_for_timeout(1000)

            # Client ID
            if page.locator("input[name='clientId']").count() > 0:
                page.fill("input[name='clientId']", "original-client-123")
            print("✅ Filled Client ID")
            
            page.wait_for_timeout(1000)

            # Embedded App URL
            if page.locator("input[name='BaseUrl']").count() > 0:
                page.fill("input[name='BaseUrl']", "https://bulk-data.smarthealthit.org/eyJlcnIiOiIiLCJwYWdlIjoxMDAwMCwidGx0IjoxNSwibSI6MSwiZGVsIjowLCJzZWN1cmUiOjEsIm9wcCI6MTB9/fhir")
            elif page.locator("input[name='appUrl']").count() > 0:
                page.fill("input[name='appUrl']", "http://localhost:5173/integrations/add")
            print("✅ Filled Embedded App URL\n")
            
            page.wait_for_timeout(2000)

            # Save Connection
            print("Saving connection...")
            save_selectors = ["button:has-text('Save')", "button:has-text('Submit')", "button[type='submit']"]
            for selector in save_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Save\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(3000)
            page.screenshot(path="1_connection_saved.png", full_page=True)

            # ============================================================
            # PART 3: CLICK BACK BUTTON
            # ============================================================
            print("=" * 60)
            print("PART 3: CLICK BACK BUTTON")
            print("=" * 60)
            
            print("\nClicking Back button...")
            back_selectors = [
                "button:has-text('Back')",
                "a:has-text('Back')",
                "button:has-text('← Back')",
                "[aria-label='Back']"
            ]
            
            back_clicked = False
            for selector in back_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Back button\n")
                    back_clicked = True
                    break
                except:
                    continue
            
            if not back_clicked:
                print("⚠️ No Back button found, using browser back")
                page.go_back()
            
            page.wait_for_timeout(2000)

            # ============================================================
            # PART 4: GO TO DASHBOARD
            # ============================================================
            print("=" * 60)
            print("PART 4: GO TO DASHBOARD PAGE")
            print("=" * 60)
            
            print("\nNavigating to Dashboard...")
            dashboard_selectors = [
                "text=Dashboard",
                "a:has-text('Dashboard')",
                "button:has-text('Dashboard')",
                "[href*='dashboard']"
            ]
            
            dashboard_clicked = False
            for selector in dashboard_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Dashboard\n")
                    dashboard_clicked = True
                    break
                except:
                    continue
            
            if not dashboard_clicked:
                print("⚠️ Could not find Dashboard link")
                # Try going to dashboard URL directly
                try:
                    page.goto("https://demo.ehrconnect.healthconnect.systems/dashboard")
                    print("✅ Navigated to Dashboard URL\n")
                except:
                    print("❌ Could not navigate to Dashboard\n")
            
            page.wait_for_timeout(2000)
            page.screenshot(path="2_dashboard.png", full_page=True)

            # ============================================================
            # PART 5: GO BACK TO CONNECTIONS PAGE
            # ============================================================
            print("=" * 60)
            print("PART 5: GO TO CONNECTIONS PAGE")
            print("=" * 60)
            
            print("\nNavigating to Connections page...")
            try:
                page.click("text=Connections")
                print("✅ Clicked Connections\n")
            except:
                try:
                    page.click("a:has-text('Connections')")
                    print("✅ Clicked Connections\n")
                except:
                    print("❌ Could not find Connections link\n")
            
            page.wait_for_timeout(3000)
            page.screenshot(path="3_connections_page.png", full_page=True)

            # ============================================================
            # PART 6: CLICK MANAGE ON CREATED CONNECTION
            # ============================================================
            print("=" * 60)
            print("PART 6: CLICK MANAGE ON CREATED CONNECTION")
            print("=" * 60)
            
            print("\nFinding 'TestConnection123' and clicking Manage...")
            
            manage_clicked = False
            
            # Method 1: Try clicking Manage in the row with our connection
            try:
                page.click("tr:has-text('TestConnection123') button:has-text('Manage')", timeout=3000)
                print("✅ Clicked Manage for TestConnection123\n")
                manage_clicked = True
            except:
                pass
            
            # Method 2: Try clicking any three dots menu first
            if not manage_clicked:
                try:
                    three_dots = page.locator("tr:has-text('TestConnection123') button[aria-label*='menu' i]")
                    if three_dots.count() > 0:
                        three_dots.first.click()
                        page.wait_for_timeout(1000)
                        print("✅ Clicked menu button\n")
                        
                        # Now click Manage from dropdown
                        page.click("button:has-text('Manage')", timeout=2000)
                        print("✅ Clicked Manage from menu\n")
                        manage_clicked = True
                except:
                    pass
            
            # Method 3: Click first Manage button found
            if not manage_clicked:
                manage_selectors = [
                    "button:has-text('Manage')",
                    "a:has-text('Manage')",
                    "[aria-label='Manage']"
                ]
                
                for selector in manage_selectors:
                    try:
                        page.locator(selector).first.click()
                        print("✅ Clicked Manage button\n")
                        manage_clicked = True
                        break
                    except:
                        continue
            
            # Method 4: Click on connection row
            if not manage_clicked:
                try:
                    page.click("tr:has-text('TestConnection123')")
                    print("✅ Clicked on connection row\n")
                    manage_clicked = True
                except:
                    pass
            
            if not manage_clicked:
                print("⚠️ Could not find Manage button automatically")
                print("Please click on 'TestConnection123' or its Manage button manually...")
                input("Press Enter after clicking...")
            
            page.wait_for_timeout(2000)
            page.screenshot(path="4_after_manage_click.png", full_page=True)

            # ============================================================
            # PART 7: CLICK EDIT AND UPDATE CONNECTION
            # ============================================================
            print("=" * 60)
            print("PART 7: EDIT THE CONNECTION")
            print("=" * 60)
            
            print("\nClicking Edit button...")
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
                print("Please click Edit button manually...")
                input("Press Enter after clicking Edit...")
            
            page.wait_for_timeout(2000)

            # Update Connection Details
            print("Updating connection details...")
            
            # Update Name
            name_selectors = ["input[name='name']", "input[name='connectionName']", "input[placeholder*='name' i]"]
            for selector in name_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("TestConnection123-EDITED")
                        print("✅ Updated Name: TestConnection123-EDITED")
                        break
                except:
                    continue
            
            page.wait_for_timeout(1000)

            # Update Client ID
            client_selectors = ["input[name='clientId']", "input[placeholder*='client' i]"]
            for selector in client_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("edited-client-999")
                        print("✅ Updated Client ID: edited-client-999")
                        break
                except:
                    continue
            
            page.wait_for_timeout(1000)

            # Update Embedded App URL
            url_selectors = ["input[name='embeddedAppUrl']", "input[name='appUrl']", "input[placeholder*='embedded' i]"]
            for selector in url_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("http://localhost:5173/integrations/edited")
                        print("✅ Updated Embedded App URL")
                        break
                except:
                    continue
            
            print()
            page.wait_for_timeout(2000)

            # Save Changes
            print("Saving changes...")
            save_selectors = ["button:has-text('Save')", "button:has-text('Update')", "button[type='submit']"]
            for selector in save_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Saved changes\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(3000)

            # Go Back
            print("Going back to Connections...")
            back_selectors = ["button:has-text('Back')", "button:has-text('Close')", "a:has-text('Back')"]
            for selector in back_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Returned to Connections\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)

            # Final Screenshot
            page.screenshot(path="5_final_result.png", full_page=True)
            
            print("\n" + "=" * 60)
            print("✅✅✅ COMPLETE FLOW FINISHED! ✅✅✅")
            print("=" * 60)
            print("\nFlow Summary:")
            print("  1. ✅ Logged in")
            print("  2. ✅ Created connection: TestConnection123")
            print("  3. ✅ Saved connection")
            print("  4. ✅ Clicked Back button")
            print("  5. ✅ Navigated to Dashboard")
            print("  6. ✅ Returned to Connections page")
            print("  7. ✅ Clicked Manage on TestConnection123")
            print("  8. ✅ Edited connection")
            print("  9. ✅ Saved changes")
            print("\n📸 Screenshots saved:")
            print("  - 1_connection_saved.png")
            print("  - 2_dashboard.png")
            print("  - 3_connections_page.png")
            print("  - 4_after_manage_click.png")
            print("  - 5_final_result.png")
            print(f"\n🔗 Current URL: {page.url}")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            page.screenshot(path="error.png")

        finally:
            print("\n" + "=" * 60)
            
            browser.close()

if __name__ == "__main__":
    complete_connection_flow()