from playwright.sync_api import sync_playwright
import time

def login_to_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()
        try:
            # STEP 1: LOGIN
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

            # STEP 2: GO TO CONNECTIONS
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

            # STEP 3: CLICK ADD NEW CONNECTIONS
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

            # STEP 4: CHOOSE EPIC
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

            # STEP 5: CHOOSE STANDALONE LAUNCH
            print("=" * 70)
            print("STEP 5: CHOOSE STANDALONE LAUNCH")
            print("=" * 70)
            standalone_clicked = False
            print("Trying Strategy 1: Radio button with label...")
            try:
                radios = page.locator("input[type='radio']").all()
                for radio in radios:
                    value = (radio.get_attribute("value") or "").lower()
                    radio_id = radio.get_attribute("id") or ""
                    if "standalone" in value or "standalone" in radio_id.lower():
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
            if not standalone_clicked:
                print("Trying Strategy 2: Label with exact text...")
                try:
                    labels = page.locator("label").all()
                    for label in labels:
                        text = label.text_content().strip()
                        text_lower = text.lower()
                        if "standalone" in text_lower and "embed" not in text_lower:
                            label.click()
                            print(f"✅ Clicked label: '{text}'\n")
                            standalone_clicked = True
                            break
                except Exception as e:
                    print(f"Strategy 2 failed: {e}")
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
            if not standalone_clicked:
                print("Trying Strategy 4: Direct text click...")
                try:
                    page.click("text='Standalone Launch'", timeout=2000)
                    print("✅ Clicked 'Standalone Launch' text\n")
                    standalone_clicked = True
                except:
                    try:
                        page.click("text=/Standalone/", timeout=2000)
                        print("✅ Clicked Standalone (partial match)\n")
                        standalone_clicked = True
                    except Exception as e:
                        print(f"Strategy 4 failed: {e}")
            if not standalone_clicked:
                print("Trying Strategy 5: Container-based selection...")
                try:
                    containers = page.locator("div, label").all()
                    for container in containers:
                        text = container.text_content().strip().lower()
                        if "standalone launch" in text and "embed" not in text:
                            radio = container.locator("input[type='radio']")
                            if radio.count() > 0:
                                radio.click()
                                print("✅ Clicked radio inside Standalone container\n")
                                standalone_clicked = True
                                break
                            else:
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
            print("=" * 70)
            print("STEP 6: ADD CONNECTION NAME")
            print("=" * 70)
            connection_name = "PerrylHealth"
            name_selectors = [
                "input[name='name']",
                "input[name='connectionName']",
                "input[placeholder*='name' i]",
                "input[placeholder*='connection name' i]"
            ]
            for selector in name_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(connection_name)
                        print(f"✅ Filled Connection Name: {connection_name}\n")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            print("=" * 70)
            print("STEP 7: ADD CLIENT ID AND CLIENT SECRET")
            print("=" * 70)
            client_id = "test-client-id-12345"
            client_id_selectors = [
                "input[name='clientId']",
                "input[name='client_id']",
                "input[placeholder*='client id' i]"
            ]
            for selector in client_id_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(client_id)
                        print(f"✅ Filled Client ID: {client_id}")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            client_secret = "test-client-secret-67890"
            client_secret_selectors = [
                "input[name='clientSecret']",
                "input[name='client_secret']",
                "input[placeholder*='client secret' i]",
                "input[type='password']"
            ]
            for selector in client_secret_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(client_secret)
                        print(f"✅ Filled Client Secret: {client_secret}\n")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            print("=" * 70)
            print("STEP 8: ADD BASE URL (FHIR ENDPOINT)")
            print("=" * 70)
            base_url = "https://r4.smarthealthit.org/"
            url_selectors = [
                "input[name='url']",
                "input[name='baseUrl']",
                "input[name='base_url']",
                "input[name='endpoint']",
                "input[name='fhirEndpoint']",
                "input[placeholder*='url' i]",
                "input[placeholder*='endpoint' i]",
                "input[placeholder*='fhir' i]"
            ]
            for selector in url_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(base_url)
                        print(f"✅ Filled Base URL: {base_url}\n")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            print("=" * 70)
            print("STEP 9: ADD OAUTH AUTHORIZATION URL")
            print("=" * 70)
            auth_url = "https://launch.smarthealthit.org/v/r4/sim/WzIsIiIsIiIsIkFVVE8iLDAsMCwwLCIiLCIiLCIiLCIiLCJhdXRoX2ludmFsaWRfY2xpZW50X2lkIiwiIiwiIiwwLDEsIiJd/auth/authorize"
            auth_url_selectors = [
                "input[name='authorizationUrl']",
                "input[name='authorization_url']",
                "input[name='authUrl']",
                "input[name='auth_url']",
                "input[name='oauthAuthUrl']",
                "input[placeholder*='authorization url' i]",
                "input[placeholder*='auth url' i]"
            ]
            for selector in auth_url_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(auth_url)
                        print(f"✅ Filled OAuth Authorization URL\n")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            print("=" * 70)
            print("STEP 10: ADD OAUTH TOKEN URL")
            print("=" * 70)
            token_url = "https://bulk-data.smarthealthit.org/auth/token"
            token_url_selectors = [
                "input[name='tokenUrl']",
                "input[name='token_url']",
                "input[name='oauthTokenUrl']",
                "input[name='oauth_token_url']",
                "input[placeholder*='token url' i]"
            ]
            for selector in token_url_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(token_url)
                        print(f"✅ Filled OAuth Token URL\n")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            print("=" * 70)
            print("STEP 11: CLICK AUTO-DETECT BUTTON")
            print("=" * 70)
            auto_detect_selectors = [
                "button:has-text('Auto-detect')",
                "button:has-text('Auto Detect')",
                "button:has-text('Detect')",
                "button:has-text('Auto-Discovery')",
                "[aria-label*='auto-detect' i]"
            ]
            auto_detect_clicked = False
            for selector in auto_detect_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click()
                        print("✅ Clicked Auto-detect button")
                        print("⏳ Waiting for auto-detection to complete...\n")
                        auto_detect_clicked = True
                        break
                except:
                    continue
            if not auto_detect_clicked:
                print("⚠️ Auto-detect button not found (may not be required)\n")
            page.wait_for_timeout(3000)
            print("=" * 70)
            print("STEP 12: ADD OAUTH SCOPES")
            print("=" * 70)
            oauth_scopes = "openid profile fhirUser launch launch/patient"
            scope_selectors = [
                "input[name='scopes']",
                "input[name='scope']",
                "input[name='oauthScopes']",
                "input[name='oauth_scopes']",
                "input[placeholder*='scope' i]",
                "textarea[name='scopes']",
                "textarea[placeholder*='scope' i]"
            ]
            scope_filled = False
            for selector in scope_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(oauth_scopes)
                        print(f"✅ Filled OAuth Scopes: {oauth_scopes}\n")
                        scope_filled = True
                        break
                except:
                    continue
            if not scope_filled:
                print("⚠️ Could not find OAuth Scopes field automatically")
                print("Please fill OAuth Scopes manually: openid profile fhirUser launch launch/patient")
                input("Press Enter after filling scopes...")
            page.wait_for_timeout(1000)
            print("=" * 70)
            print("STEP 13: ADD APPLICATION RETURN URL")
            print("=" * 70)
            return_url = "http://localhost:5173/integrations/add"
            return_url_selectors = [
                "input[name='returnUrl']",
                "input[name='return_url']",
                "input[name='redirectUrl']",
                "input[name='redirect_url']",
                "input[name='callbackUrl']",
                "input[name='embeddedAppUrl']",
                "input[name='appUrl']",
                "input[placeholder*='return url' i]",
                "input[placeholder*='redirect' i]",
                "input[placeholder*='callback' i]",
                "input[placeholder*='application url' i]"
            ]
            for selector in return_url_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(return_url)
                        print(f"✅ Filled Application Return URL: {return_url}\n")
                        break
                except:
                    continue
            page.wait_for_timeout(2000)
            print("=" * 70)
            print("STEP 14: CLICK CREATE CONNECTION")
            print("=" * 70)
            create_selectors = [
                "button:has-text('Create Connection')",
                "button:has-text('Create')",
                "button:has-text('Save')",
                "button:has-text('Submit')",
                "button[type='submit']"
            ]
            for selector in create_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Clicked Create Connection button")
                    print("⏳ Waiting for connection to be created...\n")
                    break
                except:
                    continue
            page.wait_for_timeout(4000)
            page.screenshot(path="1_connection_created.png", full_page=True)
            print("=" * 70)
            print("STEP 15: GO BACK TO DASHBOARD")
            print("=" * 70)
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
                    print("✅ Navigated to Dashboard\n")
                    dashboard_clicked = True
                    break
                except:
                    continue
            if not dashboard_clicked:
                try:
                    page.goto("https://demo.ehrconnect.healthconnect.systems/dashboard")
                    print("✅ Navigated to Dashboard via URL\n")
                except:
                    print("⚠️ Could not navigate to Dashboard\n")
            page.wait_for_timeout(2000)
            page.screenshot(path="2_dashboard.png", full_page=True)
        finally:
            browser.close()

if __name__ == "__main__":
    login_to_dashboard()
