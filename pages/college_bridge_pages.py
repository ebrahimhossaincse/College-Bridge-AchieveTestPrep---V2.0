import json
import time
import allure

from pathlib import Path
from config.settings import BASE_URL
from locators.college_bridge_locators import LandingPageLocators, StartQualifyPageLocators, MindsetQualifyPageLocators, \
    BridgeStartPageLocators, GeneralEducationPageLocators, EntranceExamPageLocators
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
        screenshot_path = take_screenshot(self.page, "landing_page_opened")
        allure.attach.file(str(screenshot_path), name="open_url", attachment_type=allure.attachment_type.PNG)


    @allure.step("Fill out and submit the College Bridge landing form")
    def fill_form_and_submit(self):
        try:
            self.select_dropdown(LandingPageLocators.PROGRAM_OF_INTEREST, self.test_data["program_of_interest"])
            self.enter_text(LandingPageLocators.FIRST_NAME, self.test_data["first_name"])
            self.enter_text(LandingPageLocators.LAST_NAME, self.test_data["last_name"])
            self.enter_text(LandingPageLocators.EMAIL_ADDRESS, self.test_data["email"])
            self.enter_text(LandingPageLocators.PHONE_NUMBER, self.test_data["phone_number"])
            self.enter_text(LandingPageLocators.ZIP_CODE, self.test_data["zip_code"])

            screenshot_path = take_screenshot(self.page, "form_filled")
            allure.attach.file(str(screenshot_path), name="form_filled", attachment_type=allure.attachment_type.PNG)

            self.click(LandingPageLocators.GET_STARTED)
            self.logger.info("Form submitted successfully.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "form_submission_failed")
            allure.attach.file(str(screenshot_path), name="form_submission_failed", attachment_type=allure.attachment_type.PNG)

            self.logger.error(f"Form submission failed: {e}")
            raise

    @allure.step("Click 'Start Qualify' button")
    def click_start_qualify_button(self):
        self.click(StartQualifyPageLocators.NEXT_BUTTON)
        screenshot_path = take_screenshot(self.page, "start_qualify_clicked")
        allure.attach.file(str(screenshot_path), name="start_qualify_clicked", attachment_type=allure.attachment_type.PNG)

    @allure.step("Complete the mindset qualification process")
    def mindset_qualify_process(self):
        try:
            self.click(MindsetQualifyPageLocators.VERY_IMPORTANT)
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.enter_text(MindsetQualifyPageLocators.ENTER_YOUR_ANSWER, "Test Lead")
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)
            time.sleep(1)
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON_INFO)

            # self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.VERY_EXCITED)
            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            self.click(MindsetQualifyPageLocators.NEXT_BUTTON)

            screenshot_path = take_screenshot(self.page, "mindset_process_completed")
            allure.attach.file(str(screenshot_path), name="mindset_process_completed", attachment_type=allure.attachment_type.PNG)
            self.logger.info("Mindset qualification process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "mindset_process_failed")
            allure.attach.file(str(screenshot_path), name="mindset_process_failed", attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Mindset qualification process failed: {e}")
            raise

    @allure.step("Complete the bridge start process")
    def bridge_start_process(self):
        try:
            self.click(BridgeStartPageLocators.NEXT_BUTTON)
            screenshot_path = take_screenshot(self.page, "bridge_start_clicked")
            allure.attach.file(str(screenshot_path), name="bridge_start_clicked",
                               attachment_type=allure.attachment_type.PNG)

        except Exception as e:
            screenshot_path = take_screenshot(self.page, "bridge_start_failed")
            allure.attach.file(str(screenshot_path), name="bridge_start_failed", attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Bridge Start process failed: {e}")
            raise

    @allure.step("Complete the general education process")
    def general_education_process(self):
        try:
            self.click(GeneralEducationPageLocators.NEXT_BUTTON)
            # self.click(GeneralEducationPageLocators.NEXT_BUTTON)
            time.sleep(1)
            self.click(GeneralEducationPageLocators.NEXT_BUTTON)
            self.click(GeneralEducationPageLocators.I_HAVE_NOT_PASSED_ANY_GEN_EDS_YET)
            self.click(GeneralEducationPageLocators.NEXT_BUTTON)
            self.click(GeneralEducationPageLocators.VERY_IMPORTANT)
            self.click(GeneralEducationPageLocators.NEXT_BUTTON)
            self.click(GeneralEducationPageLocators.NEXT_BUTTON)

            screenshot_path = take_screenshot(self.page, "general_education_process_completed")
            allure.attach.file(str(screenshot_path), name="general_education_process_completed", attachment_type=allure.attachment_type.PNG)
            self.logger.info("General Education process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "general_education_process_failed")
            allure.attach.file(str(screenshot_path), name="general_education_process_failed", attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"General Education process failed: {e}")
            raise

    @allure.step("Complete the entrance exam process")
    def entrance_exam_process(self):
        try:
            self.click(EntranceExamPageLocators.NEXT_BUTTON)
            self.click(EntranceExamPageLocators.I_HAVE_NOT_TAKEN_MY_RN_ENTRANCE_EXAM)
            self.click(EntranceExamPageLocators.NEXT_BUTTON)
            self.click(EntranceExamPageLocators.NEXT_BUTTON)
            self.click(EntranceExamPageLocators.VERY_CONCERNED)
            self.click(EntranceExamPageLocators.NEXT_BUTTON)
            self.click(EntranceExamPageLocators.NEXT_BUTTON)

            screenshot_path = take_screenshot(self.page, "entrance_exam_process_completed")
            allure.attach.file(str(screenshot_path), name="entrance_exam_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("General Education process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "entrance_exam_process_failed")
            allure.attach.file(str(screenshot_path), name="entrance_exam_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Entrance Exam process failed: {e}")
            raise


