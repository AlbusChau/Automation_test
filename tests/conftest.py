import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from utils.config_reader import ConfigReader
import allure
from allure_commons.types import AttachmentType

@pytest.fixture
def driver():
    # Launch a new Chrome browser instance
    driver = webdriver.Chrome()
    # Maximize the browser window for better visibility and to avoid issues caused by different screen sizes
    driver.maximize_window()
    # Load settings from your JSON via the ConfigReader
    base_url = ConfigReader.get_base_url()
    implicit_timeout = ConfigReader.get_timeout()
    # Apply settings
    driver.implicitly_wait(implicit_timeout)
    driver.get(base_url)
    yield driver
    # After the test finishes, close the browser and release resources
    driver.quit()


@pytest.fixture
def wait(driver):
    # Reusable explicit wait (10s) for any page/test that needs it.
    # Pass alongside `driver` and use wait.until(EC...) for SPA transitions.
    return WebDriverWait(driver, 10)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG
            )