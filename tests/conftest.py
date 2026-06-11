import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture
def driver():

    # Launch a new Chrome browser instance
    driver = webdriver.Chrome()

    # Maximize the browser window for better visibility and to avoid issues caused by different screen sizes
    driver.maximize_window()

    # Set an implicit wait of 10 seconds.
    # Selenium will wait up to 10 seconds when trying to locate elements before throwing a NoSuchElementException.
    driver.implicitly_wait(10)

    # Navigate to the OrangeHRM demo website
    driver.get("https://opensource-demo.orangehrmlive.com/")

    # Yield returns the driver object to the test case.
    # The test executes at this point.
    yield driver

    # After the test finishes, close the browser and release resources
    driver.quit()


@pytest.fixture
def wait(driver):
    # Reusable explicit wait (10s) for any page/test that needs it.
    # Pass alongside `driver` and use wait.until(EC...) for SPA transitions.
    return WebDriverWait(driver, 10)