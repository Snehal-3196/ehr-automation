from playwright.sync_api import sync_playwright
import time

def complete_epic_connection_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()

        try:
            # ============================================================
            # STEP 1: LOGIN
            # ============================================================
            print("=" * 70)
            print("STEP 1: LOGIN")
            print("=" * 70)
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
            # STEP 2: GO TO CONNECTIONS
            # ============================================================
            print("=" * 70)
            print("STEP 2: GO TO CONNECTIONS PAGE")
            print("=" * 70)
            
            try:
                page.click("text=Connections")
                print("✅ Navigated to Connections page\n")
            except:
                page.click("a:has-text('Connections')")
                print("✅ Navigated to Connections page\n")
            
            page.wait_for_timeout(2000)

            # ============================================================
            # STEP 3: CLICK ADD NEW CONNECTIONS
            # ============================================================
            print("=" * 70)
            print("STEP 3: CLICK ADD NEW CONNECTIONS BUTTON")
            print("=" * 70)
            
            add_selectors = [
                "button:has-text('Add Connection')",
                "button:has-text('Add New Connection')",
                "button:has-text('New Connection')",
                "button:has-text('Add New')",
                "button:has-text('Add')"
            ]
            
            for selector in add_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Add New Connection button\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)

            # ============================================================
            # STEP 4: CHOOSE EPIC
            # ============================================================
            print("=" * 70)
            print("STEP 4: CHOOSE EPIC")
            print("=" * 70)
            
            epic_selectors = ["text=Epic", "label:has-text('Epic')", "div:has-text('Epic')", "input[value='Epic']"]
            for selector in epic_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Selected Epic\n")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)

            # ============================================================
            # STEP 5: CHOOSE STANDALONE LAUNCH (SMART DETECTION)
            # ============================================================
            print("=" * 70)
            print("STEP 5: CHOOSE STANDALONE LAUNCH")
            print("=" * 70)
            
            standalone_clicked = False
            
            # Strategy 1: Look for radio button with "standalone" in value, then click its label
            print("Trying Strategy 1: Radio button with label...")
            try:
                radios = page.locator("input[type='radio']").all()
                for radio in radios:
                    value = (radio.get_attribute("value") or "").lower()
                    radio_id = radio.get_attribute("id") or ""
                    
                    if "standalone" in value or "standalone" in radio_id.lower():
                        # Found standalone radio, now click it or its label
                        if radio_id:
                            label = page.locator(f"label[for='{radio_id}']")
                            if label.count() > 0:
                                label.click()
                                print(f"✅ Clicked label for standalone radio (id={radio_id})\n")
                                standalone_clicked = True
                                break
                        else:
                            radio.click()
                            print("✅ Clicked standalone radio button\n")
                            standalone_clicked = True
                            break
            except Exception as e:
                print(f"Strategy 1 failed: {e}")
            
            # Strategy 2: Look for label containing "Standalone Launch" (not Embedded)
            if not standalone_clicked:
                print("Trying Strategy 2: Label with exact text...")
                try:
                    labels = page.locator("label").all()
                    for label in labels:
                        text = label.text_content().strip()
                        text_lower = text.lower()
                        
                        # Must contain "standalone" but NOT "embed"
                        if "standalone" in text_lower and "embed" not in text_lower:
                            label.click()
                            print(f"✅ Clicked label: '{text}'\n")
                            standalone_clicked = True
                            break
                except Exception as e:
                    print(f"Strategy 2 failed: {e}")
            
            # Strategy 3: Look for clickable div/span with "Standalone Launch"
            if not standalone_clicked:
                print("Trying Strategy 3: Clickable div/span...")
                try:
                    clickable_elements = page.locator("div[role='radio'], span[role='radio'], div.option, div.choice").all()
                    for elem in clickable_elements:
                        text = elem.text_content().strip().lower()
                        if "standalone" in text and "embed" not in text:
                            elem.click()
                            print(f"✅ Clicked element with text: '{text}'\n")
                            standalone_clicked = True
                            break
                except Exception as e:
                    print(f"Strategy 3 failed: {e}")
            
            # Strategy 4: Use page.click() with text selector
            if not standalone_clicked:
                print("Trying Strategy 4: Direct text click...")
                try:
                    # Try clicking on exact text
                    page.click("text='Standalone Launch'", timeout=2000)
                    print("✅ Clicked 'Standalone Launch' text\n")
                    standalone_clicked = True
                except:
                    try:
                        # Try partial match
                        page.click("text=/Standalone/", timeout=2000)
                        print("✅ Clicked Standalone (partial match)\n")
                        standalone_clicked = True
                    except Exception as e:
                        print(f"Strategy 4 failed: {e}")
            
            # Strategy 5: Find by parent container
            if not standalone_clicked:
                print("Trying Strategy 5: Container-based selection...")
                try:
                    # Look for a container that has both radio and text
                    containers = page.locator("div, label").all()
                    for container in containers:
                        text = container.text_content().strip().lower()
                        if "standalone launch" in text and "embed" not in text:
                            # Try to find and click the radio inside
                            radio = container.locator("input[type='radio']")
                            if radio.count() > 0:
                                radio.click()
                                print("✅ Clicked radio inside Standalone container\n")
                                standalone_clicked = True
                                break
                            else:
                                # Just click the container
                                container.click()
                                print("✅ Clicked Standalone container\n")
                                standalone_clicked = True
                                break
                except Exception as e:
                    print(f"Strategy 5 failed: {e}")
            
            if not standalone_clicked:
                print("⚠️ All automatic strategies failed!")
                print("Please select 'Standalone Launch' manually...")
                print("Make sure to select 'Standalone Launch' NOT 'Embedded Launch'")
                input("Press Enter after selecting Standalone Launch...")
            
            page.wait_for_timeout(2000)
            
            # Click Launch/Continue button after selecting option
            print("Clicking Launch/Continue button...")
            launch_selectors = [
                "button:has-text('Launch')",
                "button:has-text('Standalone Launch')",
                "button:has-text('Continue')",
                "button:has-text('Next')",
                "button[type='submit']"
            ]
            
            launch_clicked = False
            for selector in launch_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print(f"✅ Clicked button: {selector}\n")
                    launch_clicked = True
                    break
                except:
                    continue
            
            if not launch_clicked:
                print("⚠️ Could not find Launch button")
                print("Please click the Launch/Continue button manually...")
                input("Press Enter after clicking...")
            
            page.wait_for_timeout(3000)

        finally:
            print("\n" + "=" * 70)

            browser.close()

if __name__ == "__main__":
    complete_epic_connection_flow()