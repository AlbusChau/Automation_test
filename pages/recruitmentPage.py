import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.basePage import BasePage

class RecruitmentPage(BasePage):
    def __init__(self, driver, wait=None):
        super().__init__(driver)
        self.driver = driver
        # optional explicit wait object tests may pass in
        self.wait = wait
        # --- Navigation ---
        self.recruitment_tab = (By.XPATH, '//span[text()="Recruitment"]')
        # prefer normalize-space XPATH to avoid link text whitespace issues
        self.vacancies_tab = (By.XPATH, '//a[normalize-space()="Vacancies"] | //span[normalize-space()="Vacancies"]')
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
        # more robust XPaths for the toggles
        # Change these from 'span' to 'input'
        self.active_toggle = (By.XPATH, '//label[contains(text(), "Active")]/ancestor::div[contains(@class, "oxd-input-group")]//input[@type="checkbox"]')
        self.publish_toggle = (By.XPATH, '//label[contains(text(), "Publish in RSS Feed and Web Page")]/ancestor::div[contains(@class, "oxd-input-group")]//input[@type="checkbox"]')
        self.current_user = (By.XPATH, '//p[@class="oxd-userdropdown-name"]')
        self.log_out_link = (By.LINK_TEXT, 'Logout')
        # ensure XPath has leading '//' so it is resolved correctly
        self.search_results = (By.XPATH, '//div[@class="oxd-table-card"]')
        self.login_title = (By.XPATH, '//h5[@class="oxd-text oxd-text--h5 orangehrm-login-title"]')
        
    def navigate_vacancy_tab(self):
        print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: clicking recruitment tab')
        self.click_when_clickable(self.recruitment_tab)
        print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: clicked recruitment tab')
        try:
            print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: attempting to click vacancies tab')
            self.click_when_clickable(self.vacancies_tab)
            print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: clicked vacancies tab')
        except Exception as e:
            print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: click_when_clickable failed:', repr(e))
            # fallback: find element and click via JS
            try:
                elem = self.find_element(self.vacancies_tab)
                print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: found vacancies element, clicking via JS')
                self.driver.execute_script("arguments[0].click();", elem)
                print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: clicked vacancies via JS')
            except Exception as e2:
                print('[DEBUG] RecruitmentPage.navigate_vacancy_tab: JS click failed:', repr(e2))
                raise

    def get_page_title(self):
        # wait for the page title element to be visible and return its text
        elem = self.wait_for_visibility(self.page_title)
        return elem.text
    
    def is_add_vacancy_page(self):
        return "Add Vacancy" in self.get_page_title()
    
    def add_vacancy_name(self, vacancy_name):
        self.send_keys(self.vacancies_name, vacancy_name)
    
    def select_job_title(self, job_title_name):
        # Click the dropdown container
        # Try native select first
        try:
            if self.select_option_from_dropdown(self.job_title_dropdown, job_title_name) is None:
                raise Exception('not-native')
        except Exception:
            # Click the dropdown and wait for options to render, then click the option element
            self.click_when_clickable(self.job_title_dropdown)
            option = (By.XPATH, f'//div[@role="option"]//span[normalize-space()="{job_title_name}"]')
            # wait for the option to be visible and clickable
            self.click_when_clickable(option)

    def add_description(self, description):
        self.send_keys(self.description, description)

    def get_current_user_login(self):
        name = self.find_element(self.current_user)
        return name.text

    def add_hiring_manager(self):
        element = self.find_element(self.hiring_manager)
        element.clear()
        hiring_manager_name = self.get_current_user_login()
        element.send_keys(hiring_manager_name)
        # Try to click an exact matching suggestion first; if not present, click the first available suggestion
        exact_suggestion = (By.XPATH, f'//div[contains(@class, "oxd-autocomplete-dropdown") or @role="listbox"]//span[normalize-space()="{hiring_manager_name}"]')
        suggestion_any = (By.XPATH, '//div[contains(@class, "oxd-autocomplete-dropdown") or @role="listbox"]//span')
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "oxd-autocomplete-dropdown") or @role="listbox"]')))
            # prefer exact match
            try:
                self.click_when_clickable(exact_suggestion, timeout=2)
                return
            except Exception:
                # click first suggestion available
                try:
                    elems = self.find_elements(suggestion_any)
                    if elems:
                        elems[0].click()
                        return
                except Exception:
                    pass
        except Exception:
            # no suggestion container; fall back to keyboard
            pass

        # final fallback to keyboard selection
        time.sleep(1)
        element.send_keys(Keys.ARROW_DOWN)
        element.send_keys(Keys.ENTER)

    def add_number_of_position(self, number_of_position):
        self.send_keys(self.position_number, number_of_position)

    # def set_active_state(self, should_be_active: bool):
    #     active_toggle_input = self.find_element(self.active_toggle)
        
    #     # Check the 'checked' property of the input
    #     is_currently_active = active_toggle_input.is_selected()
        
    #     if should_be_active != is_currently_active:
    #         # Click the parent or the visual label associated with this input
    #         self.driver.execute_script("arguments[0].click();", active_toggle_input)
            
    #         # Verify the checkbox is now in the correct state
    #         WebDriverWait(self.driver, 5).until(
    #             lambda d: d.find_element(*self.active_toggle).is_selected() == should_be_active
    #         )

    # def set_publish_state(self, should_be_published: bool):
    #     publish_toggle_input = self.find_element(self.publish_toggle)
    #     is_currently_published = publish_toggle_input.is_selected()
    #     # Alternative check if the visual state is determined by a class on a parent
        
    #     if should_be_published != is_currently_published:
    #         # Use JavaScript to click
    #         self.driver.execute_script("arguments[0].click();", publish_toggle_input)

    #         # Verification - re-query element inside wait to avoid stale reference
    #         WebDriverWait(self.driver, 5).until(
    #             lambda d: d.find_element(*self.publish_toggle).get_attribute("class")) == should_be_published
        
    def add_vacancy(self, vacancy_name, job_title_name, description, number_of_position):
        print('[DEBUG] RecruitmentPage.add_vacancy: clicking Add')
        self.click_when_clickable(self.add_button)
        # wait for the add-vacancy form to appear before interacting with fields
        try:
            self.wait_for_visibility(self.vacancies_name,)
        except Exception:
            # fallback - continue and let subsequent waits/operations raise meaningful errors
            pass
        print('[DEBUG] RecruitmentPage.add_vacancy: filling vacancy name')
        self.add_vacancy_name(vacancy_name)
        print('[DEBUG] RecruitmentPage.add_vacancy: selecting job title')
        self.select_job_title(job_title_name)
        print('[DEBUG] RecruitmentPage.add_vacancy: adding description')
        self.add_description(description)
        print('[DEBUG] RecruitmentPage.add_vacancy: adding hiring manager')
        self.add_hiring_manager()
        print('[DEBUG] RecruitmentPage.add_vacancy: adding number of position')
        self.add_number_of_position(number_of_position)
        #print('[DEBUG] RecruitmentPage.add_vacancy: setting active/publish states')
        # self.set_active_state(should_be_active)
        # self.set_publish_state(should_be_published)
        self.click_when_clickable(self.save_button)

    def is_edit_vacancy_page(self):
        actual_title = self.get_page_title()
        expected_title = "Edit Vacancy"
        
        # Use an assertion for a clean, forced failure
        assert expected_title in actual_title, f"Expected page title to contain '{expected_title}', but found '{actual_title}'"
        
        return True
    
    # def is_vacancy_page(self):
    #     # Ensure we're on the vacancies page by clicking cancel if we're on add/edit (safe to try)
    #     try:
    #         self.click_when_clickable(self.cancel_button)
    #     except Exception:
    #         pass
    #     return "Vacancies" in self.get_page_title()
    
    def search_vacancies(self, job_title):
        try:
            self.click_when_clickable(self.cancel_button)
        except Exception:
            pass
        self.select_job_title(job_title)
        self.add_hiring_manager()
        self.click_when_clickable(self.search_button)
        # wait for results container to appear
        try:
            WebDriverWait(self.driver, 6).until(EC.visibility_of_element_located(self.search_results))
        except Exception:
            pass

    def verfiy_search_result(self):
        # find all matching result rows and return whether any exist
        rows = self.find_elements(self.search_results)
        return len(rows) > 0
    
    def is_log_out(self):
        self.click(self.current_user)
        self.click(self.log_out_link)
        return self.is_displayed(self.login_title)