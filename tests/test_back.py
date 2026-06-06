import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

def test_back_browser(driver):
    
    assert driver.title == 'OrangeHRM'

    driver.get('https://www.google.com')
    assert driver.title == 'Google'

    driver.back()
    tab_title = driver.title
    print(f"Title of the new tab: {tab_title}")