import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestPractice():

    def test_drag_and_drop(self, driver):
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("https://demo.guru99.com/test/drag_drop.html")
        
        # Initialize wait and actions
        wait = WebDriverWait(driver, 10)
        actions = ActionChains(driver)

        # 1. Drag BANK to Debit Account
        source1 = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()=' BANK ']")))
        target1 = wait.until(EC.visibility_of_element_located((By.XPATH, "//ol[@id='bank']/li")))
        actions.drag_and_drop(source1, target1).perform()

        # 2. Drag first 5000 to Amount (Debit side)
        source2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[@class='block13 ui-draggable'][1]")))
        target2 = wait.until(EC.visibility_of_element_located((By.XPATH, "//ol[@id='amt7']")))
        actions.drag_and_drop(source2, target2).perform()

        # 3. Drag SALES to Credit Account
        source3 = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='SALES']")))
        target3 = wait.until(EC.visibility_of_element_located((By.XPATH, "//ol[@id='loan']")))
        actions.drag_and_drop(source3, target3).perform()

        # 4. Drag second 5000 to Amount (Credit side)
        source4 = wait.until(EC.visibility_of_element_located((By.XPATH, "(//li[@class='block13 ui-draggable'][2]")))
        target4 = wait.until(EC.visibility_of_element_located((By.XPATH, "//ol[@id='amt7']")))
        actions.drag_and_drop(source4, target4).perform()

        # Observe the result
        time.sleep(5)
        driver.quit()
