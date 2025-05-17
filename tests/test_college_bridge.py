import pytest
import allure
from pages.college_bridge_pages import CollegeBridgeLandingPage

@allure.suite("College Bridge")
@allure.feature("College Bridge - Lead Creation Process")
class TestCollegeBridge:

    @pytest.fixture(autouse=True)
    def setup(self, page):  # Use 'page' instead of 'page_context'
        self.page = page
        self.landing_page = CollegeBridgeLandingPage(self.page)

    @allure.title("Open College Bridge URL")
    @pytest.mark.order(1)
    def test_open_url(self):
        with allure.step("Open the URL"):
            self.landing_page.open()

    @allure.title("Fill out College Bridge form")
    @pytest.mark.order(2)
    def test_fill_form(self):
        with allure.step("Fill the form and submit"):
            self.landing_page.fill_form_and_submit()

    @allure.title("Click Start Qualify button")
    @pytest.mark.order(3)
    def test_click_start_qualify(self):
        with allure.step("Click start qualify button"):
            self.landing_page.click_start_qualify_button()

    @allure.title("Complete Mindset Qualify Process")
    @pytest.mark.order(4)
    def test_complete_mindset(self):
        with allure.step("Complete mindset qualify process"):
            self.landing_page.mindset_qualify_process()