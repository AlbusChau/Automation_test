from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pages.basePage import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # khởi tạo driver để giúp tương tác với Chrome
        self.driver = driver
        # danh sách các locator của các element trên trang login
        self.username_field = (By.NAME, 'username')
        self.password_field = (By.NAME, 'password')
        self.click_btn = (By.XPATH, '//button[@type="submit"]')
        self.upgrade_btn = (By.XPATH, '//button[@class="oxd-glass-button orangehrm-upgrade-button"]')

    def login(self, username, password):
        self.send_keys(self.username_field, username)
        self.send_keys(self.password_field, password)
        self.click(self.click_btn)

    def is_upgrade_button_displayed(self):
        return self.is_displayed(self.upgrade_btn)