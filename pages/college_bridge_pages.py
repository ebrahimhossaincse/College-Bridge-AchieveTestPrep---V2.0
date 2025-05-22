import json
import time
import allure
from pathlib import Path
from config.settings import BASE_URL
from locators.college_bridge_locators import (
    LandingPageLocators,
    StartQualifyPageLocators,
    MindsetQualifyPageLocators,
    BridgeStartPageLocators,
    GeneralEducationPageLocators,
    EntranceExamPageLocators
)
from pages.base_page import BasePage
from utils.helpers import take_screenshot
from utils.generate_random_test_data import fetch_fake_users, save_to_json

class CollegeBridgeLandingPage(BasePage):
    TEST_DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "college_bridge_test_data.json"
    TEST_URLS = Path(__file__).resolve().parent.parent / "test_data" / "college_bridge_urls.json"

    def __init__(self, page):
        super().__init__(page)
        self.test_data = self._prepare_and_load_test_data()
        self.test_urls = self._load_json_file(self.TEST_URLS)

    def _load_json_file(self, file_path):
        """Load JSON file and handle errors."""
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                if not data:
                    raise ValueError(f"File {file_path} is empty.")
                return data
        except Exception as e:
            raise RuntimeError(f"Failed to load {file_path}: {e}")

    def _prepare_and_load_test_data(self):
        """Fetch, save, and load test data."""
        try:
            users = fetch_fake_users()
            save_to_json(users, self.TEST_DATA_FILE)
            return self._load_json_file(self.TEST_DATA_FILE)[0]  # Use first user
        except Exception as e:
            self.logger.error(f"❌ Failed to prepare or load test data: {e}")
            raise

    @allure.step("Open College Bridge Landing Page")
    def open(self):
        """Open the landing page and verify URL."""
        self.logger.info("Opening College Bridge Landing Page.")
        self.page.goto(BASE_URL, wait_until="domcontentloaded")
        if not self.compare_current_url(BASE_URL):
            raise ValueError(f"Current URL {self.page.url} does not match {BASE_URL}.")
        screenshot_path = take_screenshot(self.page, "landing_page_opened")
        allure.attach.file(str(screenshot_path), name="landing_page_opened", attachment_type=allure.attachment_type.PNG)

    @allure.step("Fill and submit College Bridge landing form")
    def fill_form_and_submit(self):
        """Fills and submits the landing page form with URL checks and retries."""
        if not self.compare_current_url(BASE_URL):
            screenshot = take_screenshot(self.page, "wrong_url")
            allure.attach.file(str(screenshot), name="wrong_url", attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Wrong URL: got {self.page.url}, expected {BASE_URL}")
            raise ValueError(f"Wrong URL: got {self.page.url}, expected {BASE_URL}")

        try:
            self.select_dropdown_with_retry(LandingPageLocators.PROGRAM_OF_INTEREST, self.test_data["program_of_interest"])
            self.enter_text_with_retry(LandingPageLocators.FIRST_NAME, self.test_data["first_name"])
            self.enter_text_with_retry(LandingPageLocators.LAST_NAME, self.test_data["last_name"])
            self.enter_text_with_retry(LandingPageLocators.EMAIL_ADDRESS, self.test_data["email"])
            self.enter_text_with_retry(LandingPageLocators.PHONE_NUMBER, self.test_data["phone_number"])
            self.enter_text_with_retry(LandingPageLocators.ZIP_CODE, self.test_data["zip_code"])

            screenshot = take_screenshot(self.page, "form_filled")
            allure.attach.file(str(screenshot), name="form_filled", attachment_type=allure.attachment_type.PNG)

            self.click_with_retry(LandingPageLocators.GET_STARTED, BASE_URL)
            self.logger.info("Form submitted successfully.")
        except Exception as e:
            screenshot = take_screenshot(self.page, "form_failed")
            allure.attach.file(str(screenshot), name="form_failed", attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Form submission failed: {e}")
            raise

    @allure.step("Click 'Start Qualify' button")
    def click_start_qualify_button(self):
        """Click the Start Qualify button with URL check and retries."""
        try:
            expected_url = self.test_urls["paths"][0]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")
            self.logger.info(f"Clicking Start Qualify button on URL {self.page.url}")
            self.click_with_retry(StartQualifyPageLocators.NEXT_BUTTON, expected_url)
            screenshot_path = take_screenshot(self.page, "start_qualify_clicked")
            allure.attach.file(str(screenshot_path), name="start_qualify_clicked", attachment_type=allure.attachment_type.PNG)
            self.logger.info("Start Qualify button clicked successfully.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "start_qualify_failed")
            allure.attach.file(str(screenshot_path), name="start_qualify_failed", attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Start Qualify button click failed: {e}")
            raise

    @allure.step("Complete the mindset qualification process")
    def mindset_qualify_process(self):
        """Complete the mindset qualification process with URL checks and retries."""
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][1], MindsetQualifyPageLocators.VERY_IMPORTANT,
                 self.click_with_retry, "Click Very Important"),
                (self.test_urls["base_url"] + self.test_urls["paths"][1], MindsetQualifyPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][2], MindsetQualifyPageLocators.ENTER_YOUR_ANSWER,
                 lambda locator, url: self.enter_text_with_retry(locator, "Test Lead"), "Enter Test Lead"),
                (self.test_urls["base_url"] + self.test_urls["paths"][2], MindsetQualifyPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][3], MindsetQualifyPageLocators.NEXT_BUTTON_INFO,
                 self.click_with_retry, "Click Next Button Info"),
                (self.test_urls["base_url"] + self.test_urls["paths"][4], MindsetQualifyPageLocators.VERY_EXCITED,
                 self.click_with_retry, "Click Very Excited"),
                (self.test_urls["base_url"] + self.test_urls["paths"][4], MindsetQualifyPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][5], MindsetQualifyPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][6], MindsetQualifyPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
            ]

            for step_index, (expected_url, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_url):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_url}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_url)

            screenshot_path = take_screenshot(self.page, "mindset_process_completed")
            allure.attach.file(str(screenshot_path), name="mindset_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Mindset qualification process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "mindset_process_failed")
            allure.attach.file(str(screenshot_path), name="mindset_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Mindset qualification process failed: {e}")
            raise

    @allure.step("Complete the bridge start process")
    def bridge_start_process(self):
        """Complete the bridge start process with URL check and retries."""
        try:
            expected_url = self.test_urls["base_url"] + self.test_urls["paths"][7]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")
            self.logger.info(f"Clicking Next button on URL {self.page.url}")
            self.click_with_retry(BridgeStartPageLocators.NEXT_BUTTON, expected_url)
            screenshot_path = take_screenshot(self.page, "bridge_start_clicked")
            allure.attach.file(str(screenshot_path), name="bridge_start_clicked",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Bridge start process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "bridge_start_failed")
            allure.attach.file(str(screenshot_path), name="bridge_start_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Bridge Start process failed: {e}")
            raise

    @allure.step("Complete the general education process")
    def general_education_process(self):
        """Complete the general education process with URL checks and retries."""
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][8], GeneralEducationPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][9], GeneralEducationPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][10], GeneralEducationPageLocators.I_HAVE_NOT_PASSED_ANY_GEN_EDS_YET,
                 self.click_with_retry, "Click I Have Not Passed Any Gen Eds Yet"),
                (self.test_urls["base_url"] + self.test_urls["paths"][10], GeneralEducationPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][11], GeneralEducationPageLocators.VERY_IMPORTANT,
                 self.click_with_retry, "Click Very Important"),
                (self.test_urls["base_url"] + self.test_urls["paths"][11], GeneralEducationPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][12], GeneralEducationPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button")
            ]

            for step_index, (expected_url, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_url):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_url}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_url)

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
        """Complete the entrance exam process with URL checks and retries for failed navigation."""
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][13], EntranceExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][14],
                 EntranceExamPageLocators.I_HAVE_NOT_TAKEN_MY_RN_ENTRANCE_EXAM, self.click_with_retry,
                 "Select RN Entrance Exam Option"),
                (self.test_urls["base_url"] + self.test_urls["paths"][14], EntranceExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][15], EntranceExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][16], EntranceExamPageLocators.VERY_CONCERNED,
                 self.click_with_retry, "Select Very Concerned"),
                (self.test_urls["base_url"] + self.test_urls["paths"][16], EntranceExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][17], EntranceExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button")
            ]

            for step_index, (expected_url, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_url):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_url}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_url)

            screenshot_path = take_screenshot(self.page, "entrance_exam_process_completed")
            allure.attach.file(str(screenshot_path), name="entrance_exam_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Entrance Exam process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "entrance_exam_process_failed")
            allure.attach.file(str(screenshot_path), name="entrance_exam_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Entrance Exam process failed: {e}")
            raise