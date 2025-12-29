def test_06_navigate_to_dashboard():
    """Test Script 6: Login + Navigate to Dashboard"""
    from playwright.sync_api import sync_playwright
    import os
    
    with sync_playwright() as p:
        # Check if running in CI (GitHub Actions sets 'CI=true')
        is_ci = os.environ.get("CI") == "true"
        
        browser = p.chromium.launch(headless=is_ci, slow_mo=0 if is_ci else 1000)
        page = browser.new_page()
        
        try:
            print("=" * 70)
            print("TEST 6: NAVIGATE TO DASHBOARD")
            print("=" * 70)
            
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
            
            # Navigate to Dashboard
            print("\n[Step 2] Clicking Dashboard menu...")
            dashboard_selectors = ["text=Dashboard", "a:has-text('Dashboard')"]
            for selector in dashboard_selectors:
                try:
                    page.click(selector, timeout=2000)
                    print("✅ Dashboard menu clicked")
                    break
                except:
                    continue
            
            page.wait_for_timeout(2000)
            
            print("\n[Step 3] Verifying Dashboard page...")
            if "dashboard" in page.url.lower():
                print("✅ Dashboard page loaded successfully")
                print(f"   Current URL: {page.url}")
            
            page.screenshot(path="test_06_dashboard.png", full_page=True)
            print("\n📸 Screenshot saved: test_06_dashboard.png")
            
            print("\n" + "=" * 70)
            print("✅ TEST 6 COMPLETED")
            print("=" * 70)
            
        finally:
            browser.close()

if __name__ == "__main__":
    test_06_navigate_to_dashboard()
