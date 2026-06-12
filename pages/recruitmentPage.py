from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RecruitmentPage:
    def __init__(self, driver):
        self.driver = driver
        # --- Navigation ---
        self.recruitment_tab = (By.XPATH, '//span[text()="Recruitment"]')
        self.vacancies_tab = (By.LINK_TEXT, "Vacancies")
        # --- Buttons ---
        self.add_button = (By.XPATH, '//button[normalize-space()="Add"]')
        self.save_button = (By.XPATH, '//button[normalize-space()="Save"]')
        self.cancel_button = (By.XPATH, '//button[normalize-space()="Cancel"]')
        self.search_button = (By.XPATH, '//button[@type="submit" and contains(., "Search")]')
        # --- Page title ---
        self.page_title = (By.XPATH, '//h6[contains(@class,"orangehrm-main-title")]')
        # --- Text inputs ---
        self.vacancies_name = (By.XPATH, '//label[contains(text(), "Vacancy Name")]/ancestor::div[contains(@class, "oxd-input-group")]//input')
        self.description = (By.XPATH, '//div[contains(@class, "oxd-input-group")][.//label[text()="Description"]]//textarea')
        self.hiring_manager = (By.XPATH, '//div[contains(@class, "oxd-input-group")][.//label[contains(text(), "Hiring Manager")]]//input')
        self.position_number = (By.XPATH, '//div[contains(@class, "oxd-input-group")][.//label[contains(text(), "Number of Positions")]]//input')
        # --- Job Title dropdown ---
        self.job_title_dropdown = (By.XPATH, 
            '//label[text()="Job Title"]/ancestor::div[contains(@class, "oxd-input-group")]//div[contains(@class, "oxd-select-wrapper")]/div[contains(@class, "oxd-select-text")]')
        # --- Toggles ---
        self.active_toggle = (By.XPATH, '//div[contains(@class, "oxd-input-group")][.//label[contains(text(), "Active")]]''//span[contains(@class, "oxd-switch-input")]')
        self.publish_toggle = (By.XPATH, 
            '//div[contains(@class, "oxd-input-group")][.//label[contains(text(), "Publish in RSS Feed and Web Page")]]''//span[contains(@class, "oxd-switch-input")]')
        
    def navigate_vacancy_tab(self):
        self.driver.find_element(*self.recruitment_tab).click()
        self.driver.find_element(*self.vacancies_tab).click()

    def get_page_title(self):
        return self.driver.find_element(*self.page_title).text
    
    def is_add_vacancy_page(self):
        return "Add Vacancy" in self.get_page_title()
    
    def add_vacancy_name(self, vacancy_name):
        self.driver.find_element(*self.vacancies_name).send_keys(vacancy_name)
    
    def select_job_title(self, job_title_name):
        # Click the dropdown container
        self.driver.find_element(*self.job_title_dropdown).click()
        
        # Select the option by its text content directly
        # This is safe because it uses the text to find the element
        option = (By.XPATH, f'//div[@role="option"]//span[text()="{job_title_name}"]')
        self.driver.find_element(*option).click()

    def add_description(self, description):
        self.driver.find_element(*self.description).send_keys(description)

    def add_hiring_manager(self, hiring_manager):
        element = self.driver.find_element(*self.hiring_manager)
        element.clear()
        element.send_keys(hiring_manager)
        option_xpath = (By.XPATH, f'//div[contains(@class, "oxd-input-group")][.//label[contains(text(), "{hiring_manager}")]]//input')
        wait = WebDriverWait(self.driver, 10)
        option = wait.until(EC.element_to_be_clickable(option_xpath))
        option.click()

    def add_number_of_position(self, number_of_position):
        self.driver.find_element(*self.position_number).send_keys(number_of_position)

    def set_active_state(self, should_be_active: bool):
        # Find the element
        toggle = self.driver.find_element(*self.active_toggle)
        # Check if currently active by looking at the class name
        is_currently_active = "oxd-switch-input--active" in toggle.get_attribute("class")
        # Only click if the current state doesn't match the desired state
        if should_be_active != is_currently_active:
            toggle.click()

    def set_publish_state(self, should_be_published: bool):
        # Find the element
        toggle = self.driver.find_element(*self.publish_toggle)
        # Check if currently active by looking at the class name
        is_currently_published = "oxd-switch-input--active" in toggle.get_attribute("class")
        # Only click if the current state doesn't match the desired state
        if should_be_published != is_currently_published:
            toggle.click()
        
    def add_vacancy(self, vacancy_name, job_title_name, description, hiring_manager, number_of_position, should_be_active, should_be_published):
        self.add_vacancy_name(vacancy_name)
        self.select_job_title(job_title_name)
        self.add_description(description)
        self.add_hiring_manager(hiring_manager)
        self.add_number_of_position(number_of_position)
        self.set_active_state(should_be_active)
        self.set_publish_state(should_be_published)
        self.driver.find_element(*self.save_button).click()

    def is_edit_vacancy_page(self):
        return "Edit Vacancy" in self.get_page_title()
    
    def is_vacancy_page(self):
        self.driver.find_element(*self.cancel_button).click()  # Ensure we're on the vacancies page by clicking cancel if we're on add/edit
        return "Vacancies" in self.get_page_title()
    
    def search_vacancies(self, job_title, hiring_manager):
        self.select_job_title(job_title)
        self.add_hiring_manager(hiring_manager)
        self.driver.find_element(*self.search_button).click()