import pytest
import allure
from playwright.sync_api import sync_playwright
import pytest
import allure
from playwright.sync_api import sync_playwright


@allure.title("Manage PerrylHealth and Test Connection")
def test_manage_and_test_connection():
    """
    Pytest + Allure version of Test Script 9: Manage PerrylHealth and Test Connection
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        try:
            with allure.step("Login to EHRConnect"):
                page.goto("https://demo.ehrconnect.healthconnect.systems/login")
                page.wait_for_load_state("networkidle")
                page.fill("#username", "administrator")
                page.fill("#password", "Mindbowser@123")
                try:
                    page.click("button[type='submit']")
                except:
                    page.click("button")
                page.wait_for_timeout(3000)

            with allure.step("Go to Connections page"):
                try:
                    page.click("text=Connections")
                except:
                    page.click("a:has-text('Connections')")
                page.wait_for_timeout(3000)
                allure.attach(page.screenshot(), name="Connections Page", attachment_type=allure.attachment_type.PNG)

            with allure.step("Click Manage for PerrylHealth"):
                manage_clicked = False
                try:
                    page.click("tr:has-text('PerrylHealth') button:has-text('Manage')", timeout=3000)
                    manage_clicked = True
                except:
                    pass
                if not manage_clicked:
                    try:
                        menu_btn = page.locator("tr:has-text('PerrylHealth') button[aria-label*='menu' i]")
                        if menu_btn.count() > 0:
                            menu_btn.first.click()
                            page.wait_for_timeout(1000)
                            page.click("button:has-text('Manage')")
                            manage_clicked = True
                    except:
                        pass
                if not manage_clicked:
                    try:
                        connection_row = page.locator("tr:has-text('PerrylHealth')").first
                        if connection_row.count() > 0:
                            manage_btn = connection_row.locator("button:has-text('Manage')").first
                            if manage_btn.count() > 0:
                                manage_btn.click()
                                manage_clicked = True
                    except:
                        pass
                if not manage_clicked:
                    try:
                        page.click("tr:has-text('PerrylHealth')", timeout=2000)
                        manage_clicked = True
                    except:
                        pass
                assert manage_clicked, "Could not find Manage button for PerrylHealth"
                page.wait_for_timeout(2000)
                allure.attach(page.screenshot(), name="Manage Clicked", attachment_type=allure.attachment_type.PNG)

            with allure.step("Open Edit page"):
                edit_clicked = False
                edit_selectors = [
                    "button:has-text('Edit')",
                    "a:has-text('Edit')",
                    "[aria-label='Edit']",
                    ".edit-button",
                    "button[title='Edit']"
                ]
                for selector in edit_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.click()
                            edit_clicked = True
                            break
                    except:
                        continue
                assert edit_clicked, "Could not find Edit button"
                page.wait_for_timeout(2000)
                allure.attach(page.screenshot(), name="Edit Page Opened", attachment_type=allure.attachment_type.PNG)

            with allure.step("Scroll down to Test Connection button"):
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(1000)
                allure.attach(page.screenshot(), name="Scrolled Down", attachment_type=allure.attachment_type.PNG)

            with allure.step("Click Test Connection button"):
                test_connection_clicked = False
                test_connection_selectors = [
                    "button:has-text('Test Connection')",
                    "button:has-text('Test')",
                    "a:has-text('Test Connection')",
                    "[aria-label*='test connection' i]",
                    "button[title*='test connection' i]",
                    ".test-connection-button",
                    "button.btn-test"
                ]
                for selector in test_connection_selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            button = page.locator(selector).first
                            button.scroll_into_view_if_needed()
                            page.wait_for_timeout(500)
                            button.click()
                            test_connection_clicked = True
                            break
                    except:
                        continue
                assert test_connection_clicked, "Could not find Test Connection button"
                page.wait_for_timeout(3000)
                allure.attach(page.screenshot(), name="Test Connection Clicked", attachment_type=allure.attachment_type.PNG)

            with allure.step("Check test connection result"):
                success_messages = [
                    "text=Connection successful",
                    "text=Test successful",
                    "text=Connected successfully",
                    "[class*='success']",
                    ".alert-success"
                ]
                error_messages = [
                    "text=Connection failed",
                    "text=Test failed",
                    "text=Error",
                    "[class*='error']",
                    ".alert-error"
                ]
                result_found = False
                for selector in success_messages:
                    try:
                        msg = page.locator(selector)
                        if msg.count() > 0 and msg.is_visible():
                            msg_text = msg.text_content()
                            allure.attach(msg_text, name="Success Message", attachment_type=allure.attachment_type.TEXT)
                            result_found = True
                            break
                    except:
                        continue
                if not result_found:
                    for selector in error_messages:
                        try:
                            msg = page.locator(selector)
                            if msg.count() > 0 and msg.is_visible():
                                msg_text = msg.text_content()
                                allure.attach(msg_text, name="Error Message", attachment_type=allure.attachment_type.TEXT)
                                result_found = True
                                break
                        except:
                            continue
                if not result_found:
                    allure.attach("No explicit success/error message found", name="No Result Message", attachment_type=allure.attachment_type.TEXT)
                allure.attach(page.screenshot(), name="Test Connection Result", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            allure.attach(str(e), name="Unexpected Error", attachment_type=allure.attachment_type.TEXT)
            page.screenshot(path="error_unexpected.png", full_page=True)
            allure.attach.file("error_unexpected.png", name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
            raise
        finally:
            browser.close()