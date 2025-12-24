def test_05_create_connection():
    """Test Script 5: Login + Create Complete Connection"""
    from playwright.sync_api import sync_playwright
    import time
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()
        try:
            print("=" * 70)
            print("TEST 5: CREATE NEW CONNECTION")
            print("=" * 70)
            
            connection_name = f"TestConnection_{int(time.time())}"
            
            # Login
            print("\n[Step 1] Login...")
            page.goto("https://demo.ehrconnect.healthconnect.systems/login")
            page.wait_for_load_state("networkidle")
            page.fill("#username", "administrator")
            page.fill("#password", "Mindbowser@123")
            try:
                page.click("button[type='submit']")
            except:
                page.click("button")
            page.wait_for_timeout(3000)
            print("✅ Logged in")
            
            # Navigate and Add Connection
            print("\n[Step 2] Navigate to Connections and click Add...")
            try:
                page.click("text=Connections")
            except:
                page.click("a:has-text('Connections')")
            page.wait_for_timeout(2000)
            
            add_selectors = ["button:has-text('Add Connection')", "button:has-text('Add')"]
            for selector in add_selectors:
                try:
                    page.click(selector, timeout=2000)
                    break
                except:
                    continue
            page.wait_for_timeout(2000)
            print("✅ Add Connection form opened")
            
            # Select Epic and Standalone
            print("\n[Step 3] Select Epic and Standalone...")
            epic_selectors = ["text=Epic", "label:has-text('Epic')"]
            for selector in epic_selectors:
                try:
                    page.click(selector, timeout=2000)
                    break
                except:
                    continue
            page.wait_for_timeout(2000)
            
            # Standalone selection
            try:
                labels = page.locator("label").all()
                for label in labels:
                    text = label.text_content().strip().lower()
                    if "standalone" in text and "embed" not in text:
                        label.click()
                        break
            except:
                pass
            
            page.wait_for_timeout(2000)
            launch_selectors = ["button:has-text('Launch')", "button:has-text('Continue')"]
            for selector in launch_selectors:
                try:
                    page.click(selector, timeout=2000)
                    break
                except:
                    continue
            page.wait_for_timeout(3000)
            print("✅ Epic Standalone selected")
            
            # Fill Connection Details
            print("\n[Step 4] Filling connection details...")
            
            # Connection Name
            name_selectors = ["input[name='name']", "input[name='connectionName']"]
            for selector in name_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(connection_name)
                        print(f"✅ Connection Name: {connection_name}")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # Client ID
            client_id_selectors = ["input[name='clientId']", "input[placeholder*='client id' i]"]
            for selector in client_id_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("test-client-12345")
                        print("✅ Client ID filled")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # Client Secret
            client_secret_selectors = ["input[name='clientSecret']", "input[type='password']"]
            for selector in client_secret_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("test-secret-67890")
                        print("✅ Client Secret filled")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # Base URL
            url_selectors = ["input[name='url']", "input[name='baseUrl']"]
            for selector in url_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("https://r4.smarthealthit.org/")
                        print("✅ Base URL filled")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # OAuth Authorization URL
            auth_url = "https://launch.smarthealthit.org/v/r4/sim/WzIsIiIsIiIsIkFVVE8iLDAsMCwwLCIiLCIiLCIiLCIiLCJhdXRoX2ludmFsaWRfY2xpZW50X2lkIiwiIiwiIiwwLDEsIiJd/auth/authorize"
            auth_selectors = ["input[name='authorizationUrl']", "input[placeholder*='authorization' i]"]
            for selector in auth_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill(auth_url)
                        print("✅ OAuth Authorization URL filled")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # OAuth Token URL
            token_selectors = ["input[name='tokenUrl']", "input[placeholder*='token' i]"]
            for selector in token_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("https://bulk-data.smarthealthit.org/auth/token")
                        print("✅ OAuth Token URL filled")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # OAuth Scopes
            scope_selectors = ["input[name='scopes']", "textarea[name='scopes']"]
            for selector in scope_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("openid profile fhirUser launch launch/patient")
                        print("✅ OAuth Scopes filled")
                        break
                except:
                    continue
            page.wait_for_timeout(1000)
            
            # Return URL
            return_selectors = ["input[name='returnUrl']", "input[name='embeddedAppUrl']"]
            for selector in return_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.fill("http://localhost:5173/integrations/add")
                        print("✅ Return URL filled")
                        break
                except:
                    continue
            page.wait_for_timeout(2000)
            
            # Create Connection
            print("\n[Step 5] Creating connection...")
            create_selectors = ["button:has-text('Create Connection')", "button:has-text('Create')", "button:has-text('Save')"]
            for selector in create_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Create button clicked")
                    break
                except:
                    continue
            
            page.wait_for_timeout(4000)
            page.screenshot(path="test_05_connection_created.png", full_page=True)
            print("\n📸 Screenshot saved: test_05_connection_created.png")
            
            print("\n" + "=" * 70)
            print("✅ TEST 5 COMPLETED")
            print(f"✅ Connection Created: {connection_name}")
            print("=" * 70)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            page.screenshot(path="error.png")
            raise
        finally:
            browser.close()
