import pytest
from selenium import webdriver
from utils.config_reader import ConfigReader
#import allure
#from allure_commons.types import AttachmentType
from selenium.webdriver.chrome.options import Options

@pytest.fixture()
def driver():
    chrome_options = Options()

    # Apply headless settings from your ConfigReader
    if ConfigReader.is_headless():
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(ConfigReader.get_base_url())
    # Optional: Set implicit wait from config
    driver.implicitly_wait(ConfigReader.get_timeout())

    yield driver
    
    # Teardown
    driver.quit()


# @pytest.fixture
# def wait(driver):
#     # Reusable explicit wait (10s) for any page/test that needs it.
#     # Pass alongside `driver` and use wait.until(EC...) for SPA transitions.
#     return WebDriverWait(driver, 10)

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call" and report.failed:
#         driver = item.funcargs.get("driver")
#         if driver:
#             allure.attach(
#                 driver.get_screenshot_as_png(),
#                 name="Failure Screenshot",
#                 attachment_type=AttachmentType.PNG
#             )