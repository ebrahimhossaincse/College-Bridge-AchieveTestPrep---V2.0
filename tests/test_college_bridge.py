import pytest
import allure
from pages.college_bridge_pages2 import CollegeBridgeLandingPage

@allure.suite("College Bridge")
@allure.feature("College Bridge - Lead Creation Process")
class TestCollegeBridge:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page
        self.landing_page = CollegeBridgeLandingPage(self.page)

    @allure.title("Open College Bridge URL")
    @pytest.mark.order(1)
    @pytest.mark.dependency()
    def test_open_url(self):
        with allure.step("Open the URL"):
            self.landing_page.open()

    @allure.title("Fill out College Bridge form")
    @pytest.mark.order(2)
    @pytest.mark.dependency(depends=["test_open_url"])
    def test_fill_form(self):
        with allure.step("Fill the form and submit"):
            self.landing_page.fill_form_and_submit()

    @allure.title("Click Start Qualify button")
    @pytest.mark.order(3)
    @pytest.mark.dependency(depends=["test_fill_form"])
    def test_click_start_qualify(self):
        with allure.step("Click start qualify button"):
            self.landing_page.click_start_qualify_button()

    @allure.title("Complete Mindset Qualify Process")
    @pytest.mark.order(4)
    @pytest.mark.dependency(depends=["test_click_start_qualify"])
    def test_complete_mindset(self):
        with allure.step("Complete mindset qualify process"):
            self.landing_page.mindset_qualify_process()

    @allure.title("Complete Bridge Start Process")
    @pytest.mark.order(5)
    @pytest.mark.dependency(depends=["test_complete_mindset"])
    def test_complete_bridge_start(self):
        with allure.step("Complete bridge start process"):
            self.landing_page.bridge_start_process()

    @allure.title("Complete General Education Process")
    @pytest.mark.order(6)
    @pytest.mark.dependency(depends=["test_complete_bridge_start"])
    def test_complete_general_education(self):
        with allure.step("Complete general education process"):
            self.landing_page.general_education_process()

    @allure.title("Complete Entrance Exam Process")
    @pytest.mark.order(7)
    @pytest.mark.dependency(depends=["test_complete_general_education"])
    def test_complete_entrance_exam(self):
        with allure.step("Complete entrance exam process"):
            self.landing_page.entrance_exam_process()