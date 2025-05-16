import pytest
import allure
from pages.college_bridge_pages import CollegeBridgeLandingPage

@allure.suite("College Bridge")
@allure.feature("College Bridge Landing Page")
class TestCollegeBridge:
    @allure.tag("positive", "smoke")
    @pytest.mark.order(1)
    def test_college_bridge(self, page):
        landing_page = CollegeBridgeLandingPage(page)
        landing_page.open()
        landing_page.fill_form_and_submit()
        landing_page.click_start_qualify_button()
        landing_page.mindset_qualify_process()
