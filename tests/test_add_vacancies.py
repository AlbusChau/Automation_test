from utils.config_reader import ConfigReader
from pages.loginPage import LoginPage
from pages.recruitmentPage import RecruitmentPage

class TestAddVacancy:
    def test_add_vacancy(self, driver):
        #Login
        login_page = LoginPage(driver)
        login_page.login(ConfigReader.get_username(), ConfigReader.get_password())
        #Navigate to Recruitment page
        recruitment_page = RecruitmentPage(driver)
        recruitment_page.navigate_vacancy_tab()
        recruitment_page.add_vacancy("Test1234", "Automation Tester", "test", "1", False, True)
        recruitment_page.is_vacancy_page()
        recruitment_page.search_vacancies("Automation Test")
        recruitment_page.verfiy_search_result()
        assert  recruitment_page.is_log_out()

