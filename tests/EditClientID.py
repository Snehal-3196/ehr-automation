import pytest
import allure
from playwright.sync_api import sync_playwright

class TestEditClientID:
    @staticmethod
    def get_client_id_selectors():
        return [
            "input[name='clientId']",
            "input[name='client_id']",
            "input[placeholder*='client id' i]"
        ]

    @allure.title("Edit Client ID for PerrylHealth connection")
    def test_edit_client_id(self):
        connection_name = "PerrylHealth"
        new_client_id = "edited-client-id-99999"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=800)
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
                    page.wait_for_timeout(2000)

                with allure.step(f"Click Manage for {connection_name}"):
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
                    assert manage_clicked, f"Could not find Manage button for '{connection_name}'"
                    page.wait_for_timeout(2000)

                with allure.step("Click Edit button"):
                    edit_selectors = [
                        "button:has-text('Edit')",
                        "a:has-text('Edit')",
                        "[aria-label='Edit']",
                        ".edit-button"
                    ]
                    edit_clicked = False
                    for selector in edit_selectors:
                        try:
                            # Scroll into view before clicking Edit
                            page.locator(selector).first.scroll_into_view_if_needed()
                            page.wait_for_timeout(500)
                            page.locator(selector).first.click()
                            edit_clicked = True
                            break
                        except:
                            continue
                    assert edit_clicked, "Could not find Edit button"
                    page.wait_for_timeout(2000)

                with allure.step(f"Edit Client ID to {new_client_id}"):
                    client_id_selectors = self.get_client_id_selectors()
                    client_id_changed = False
                    for selector in client_id_selectors:
                        try:
                            if page.locator(selector).count() > 0:
                                # Scroll into view before editing Client ID
                                page.locator(selector).first.scroll_into_view_if_needed()
                                page.wait_for_timeout(500)
                                page.locator(selector).first.fill(new_client_id)
                                client_id_changed = True
                                break
                        except:
                            continue
                    assert client_id_changed, f"Could not change Client ID to {new_client_id}"
                    page.wait_for_timeout(1000)

                with allure.step("Save changes"):
                    save_selectors = [
                        "button:has-text('Save')",
                        "button:has-text('Update')",
                        "button:has-text('Submit')",
                        "button[type='submit']"
                    ]
                    saved = False
                    for selector in save_selectors:
                        try:
                            page.click(selector, timeout=2000)
                            saved = True
                            break
                        except:
                            continue
                    assert saved, "Could not save changes"
                    page.wait_for_timeout(2000)
                    allure.attach(page.url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(str(e), name="Error", attachment_type=allure.attachment_type.TEXT)
                page.screenshot(path="error.png")
                allure.attach.file("error.png", name="Error Screenshot", attachment_type=allure.attachment_type.PNG)
                raise
            finally:
                browser.close()
