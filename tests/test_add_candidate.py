from pages.loginPage import LoginPage
from pages.recruitmentPage import RecruitmentPage

class TestAddCandidate():
    def test_add_candidate(self, driver, wait):
        login_page = LoginPage(driver)
        login_page.login("Admin","admin123")
        recruitment_page = RecruitmentPage(driver, wait)
        recruitment_page.navigate()
        recruitment_page.add_candidate("John", "Doe", "johndoe@gmail.com")
        assert recruitment_page.get_saved_candidate_name() == "John Doe"