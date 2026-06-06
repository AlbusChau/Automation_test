import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
def test_login(driver):
    # Define locator for the username input field
    username_field = (By.NAME, "username")

    # Define locator for the password input field
    password_field = (By.NAME, "password")

    # Define locator for the Login button
    click_button = (By.XPATH, '//button[@type="submit"]')

    # Define locator for the Upgrade button displayed after successful login
    # This element exists on the dashboard page
    upgrade_button = (By.XPATH, '//button[@class="oxd-glass-button orangehrm-upgrade-button"]')

    # Enter username into the username textbox
    driver.find_element(*username_field).send_keys("Admin")

    # Enter password into the password textbox
    driver.find_element(*password_field).send_keys("admin123")

    # Click the Login button
    driver.find_element(*click_button).click()

    # Verification step:
    # Check that the Upgrade button is visible.
    # If the button is displayed, login is considered successful.
    assert driver.find_element(*upgrade_button).is_displayed()