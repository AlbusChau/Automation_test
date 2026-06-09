from pages.loginPage import LoginPage


class TestLogin:

    def test_login(self, driver):
        login_page = LoginPage(driver)
        login_page.login("Admin", "admin123")
        # Assert the upgrade button is visible after login
        assert login_page.is_upgrade_button_displayed()