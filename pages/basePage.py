from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

DEFAULT_WAIT = 10

class BasePage:
    def __init__(self, driver):
        # khởi tạo driver để giúp tương tác với Chrome
        self.driver = driver

    def find_element(self, locator):
        return WebDriverWait(self.driver, DEFAULT_WAIT).until(lambda d: d.find_element(*locator))

    def click(self, locator):
        self.find_element(locator).click()

    def click_when_clickable(self, locator, timeout=DEFAULT_WAIT):
        WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator)).click()

    def wait_for_visibility(self, locator, timeout=DEFAULT_WAIT):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

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