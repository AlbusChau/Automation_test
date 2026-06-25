import pytest
from pages.loginPage import LoginPage
from utils.config_reader import ConfigReader
class TestLogin:
    @pytest.mark.smoke
    def test_login(self, driver):
        login_page = LoginPage(driver)
        # Fetch credentials from the JSON file via ConfigReader
        username = ConfigReader.get_username()
        password = ConfigReader.get_password()
        # Use the fetched credentials to log in
        login_page.login(username, password)
        # Assert the upgrade button is visible after login
        assert login_page.is_upgrade_button_displayed()