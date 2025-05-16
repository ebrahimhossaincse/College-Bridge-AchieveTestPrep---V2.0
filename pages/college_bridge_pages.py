import json
import time
import allure

from pathlib import Path
from config.settings import BASE_URL
from locators.college_bridge_locators import LandingPageLocators, StartQualifyPageLocators, MindsetQualifyPageLocators
from pages.base_page import BasePage
from utils.helpers import take_screenshot
from utils.generate_random_test_data import fetch_fake_users, save_to_json


class CollegeBridgeLandingPage(BasePage):
    TEST_DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "college_bridge_test_data.json"

    def __init__(self, page):
        super().__init__(page)
        self.test_data = self._prepare_and_load_test_data()

    def _prepare_and_load_test_data(self):
        """Fetch and save new test data, then load it."""
        try:
            users = fetch_fake_users()
            save_to_json(users)
            return self._load_test_data()
        except Exception as e:
            self.logger.error(f"❌ Failed to prepare or load test data: {e}")
            raise

    def _load_test_data(self):
        try:
            with open(self.TEST_DATA_FILE, "r") as file:
                data = json.load(file)
                if not data:
                    raise ValueError("Test data file is empty.")
                return data[0]  # Using first user
        except Exception as e:
            raise RuntimeError(f"Failed to load test data: {e}")

    def open(self):
        self.logger.info("Opening College Bridge Landing Page.")
        self.page.goto(BASE_URL, wait_until="domcontentloaded")

    @allure.step("Fill out and submit the College Bridge landing form")
    def fill_form_and_submit(self):
        try:
            self.select_dropdown(LandingPageLocators.PROGRAM_OF_INTEREST, self.test_data["program_of_interest"])
            self.enter_text(LandingPageLocators.FIRST_NAME, self.test_data["first_name"])
            self.enter_text(LandingPageLocators.LAST_NAME, self.test_data["last_name"])
            self.enter_text(LandingPageLocators.EMAIL_ADDRESS, self.test_data["email"])
            self.enter_text(LandingPageLocators.PHONE_NUMBER, self.test_data["phone_number"])
            self.enter_text(LandingPageLocators.ZIP_CODE, self.test_data["zip_code"])

            take_screenshot(self.page, "form_filled")

            self.click(LandingPageLocators.GET_STARTED)
            self.logger.info("Form submitted successfully.")
        except Exception as e:
            take_screenshot(self.page, "form_submission_failed")
            self.logger.error(f"Form submission failed: {e}")
            raise

    @allure.step("Click 'Start Qualify' button")
    def click_start_qualify_button(self):
        self.click(StartQualifyPageLocators.NEXT_BUTTON)
        take_screenshot(self.page, "start_qualify_clicked")

    @allure.step("Complete the mindset qualification process")
    def mindset_qualify_process(self):
        try:
            self.click(MindsetQualifyPageLocators.VERY_IMPORTANT)
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.enter_text(MindsetQualifyPageLocators.ENTER_YOUR_ANSWER, "Test Lead")
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.VERY_EXCITED)
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            take_screenshot(self.page, "mindset_process_completed")
            self.logger.info("Mindset qualification process completed.")
        except Exception as e:
            take_screenshot(self.page, "mindset_process_failed")
            self.logger.error(f"Mindset qualification process failed: {e}")
            raise
