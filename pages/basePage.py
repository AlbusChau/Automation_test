from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

class BasePage:
    def __init__(self, driver):
        # khởi tạo driver để giúp tương tác với Chrome
        self.driver = driver

    def find_element(self, locator):
        return WebDriverWait(self.driver, 10).until(lambda d: d.find_element(*locator))

    def click(self, locator):
        self.find_element(locator).click()

    def send_keys(self, locator, text):
        self.find_element(locator).send_keys(text)

    def is_displayed(self, locator):
        return self.find_element(locator).is_displayed()

    def select_option_from_dropdown(self, dropdown_locator, option_text):
        dropdown = self.find_element(dropdown_locator)
        # Try native <select> first
        try:
            select = Select(dropdown)
            # try select by visible text
            select.select_by_visible_text(option_text)
            return
        except Exception:
            # Not a native select element - fall back to clicking
            return None