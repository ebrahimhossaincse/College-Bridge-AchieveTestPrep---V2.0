import json
import time
import allure
from pathlib import Path
from config.settings import BASE_URL, PREBUY, DECISION
from locators.college_bridge_locators import (
    LandingPageLocators,
    StartQualifyPageLocators,
    MindsetQualifyPageLocators,
    BridgeStartPageLocators,
    GeneralEducationPageLocators,
    EntranceExamPageLocators, CoreNursingPageLocators, ExitExamPageLocators, ConfirmContactPageLocators,
    ResultsPageLocators, CollegePlanPageLocators, PreBuyOrNotPreBuyOptionsPageLocators, PreBuyCheckoutPageLocators,
    PreBuyPurchasedPageLocators, ReadinessPageLocators, ReadySoonThanksPageLocators, ReadyNotYetVideoPageLocators,
    ReadyNotYetThanksPageLocators
)
from pages.base_page import BasePage
from utils.helpers import take_screenshot
from utils.generate_random_test_data import fetch_fake_users, save_to_json, clean_phone_number


class CollegeBridgeLandingPage(BasePage):
    TEST_DATA_FILE = Path(__file__).resolve().parent.parent / "test_data" / "college_bridge_test_data.json"
    TEST_URLS = Path(__file__).resolve().parent.parent / "test_data" / "college_bridge_urls.json"
    TEST_CARDS = Path(__file__).resolve().parent.parent / "test_data" / "test_card.json"

    # Prepare fresh test data once per test run at the class level
    try:
        # Delete existing test data file to force regeneration
        if TEST_DATA_FILE.exists():
            TEST_DATA_FILE.unlink()
        # Generate and save new test data
        users = fetch_fake_users(quantity=1)  # Generate one user
        save_to_json(users, TEST_DATA_FILE)  # Save to JSON file
        with open(TEST_DATA_FILE, "r") as file:
            TEST_DATA = json.load(file)[0]  # Load first user

    except Exception as e:
        raise RuntimeError(f"Failed to prepare or load test data: {e}")

    def __init__(self, page):
        super().__init__(page)
        self.test_data = self.TEST_DATA  # Use class-level test data
        self.test_urls = self._load_json_file(self.TEST_URLS)
        self.test_cards = self._load_json_file(self.TEST_CARDS)

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

    @allure.step("Complete the core nursing process")
    def core_nursing_process(self):
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][18], CoreNursingPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][19],
                 CoreNursingPageLocators.I_HAVE_NOT_TAKEN_MY_CORE_RN_COURSES, self.click_with_retry,
                 "Select I Have Not Taken My Core RN Courses Option"),
                (self.test_urls["base_url"] + self.test_urls["paths"][19], CoreNursingPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][20], CoreNursingPageLocators.VERY_CONCERNED,
                 self.click_with_retry, "Select Very Concerned"),
                (self.test_urls["base_url"] + self.test_urls["paths"][20], CoreNursingPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][21], CoreNursingPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][22], CoreNursingPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button")
            ]

            for step_index, (expected_url, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_url):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_url}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_url)

            screenshot_path = take_screenshot(self.page, "core_nursing_process_completed")
            allure.attach.file(str(screenshot_path), name="core_nursing_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Core Nursing process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "core_nursing_process_failed")
            allure.attach.file(str(screenshot_path), name="core_nursing_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Core Nursing process failed: {e}")
            raise

    @allure.step("Exit Exam process")
    def exit_exam_process(self):
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][23], ExitExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][24],
                 ExitExamPageLocators.I_HAVE_NOT_TAKEN_THE_NCLEX_RN_YET, self.click_with_retry,
                 "Select I Have Not Taken My Core RN Courses Option"),
                (self.test_urls["base_url"] + self.test_urls["paths"][24], ExitExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][25], ExitExamPageLocators.VERY_CONCERNED,
                 self.click_with_retry, "Select Very Concerned"),
                (self.test_urls["base_url"] + self.test_urls["paths"][25], ExitExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][26], ExitExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][27], ExitExamPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button")
            ]

            for step_index, (expected_url, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_url):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_url}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_url)

            screenshot_path = take_screenshot(self.page, "exit_exam_process_completed")
            allure.attach.file(str(screenshot_path), name="exit_exam_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Exit Exam process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "exit_exam_process_failed")
            allure.attach.file(str(screenshot_path), name="exit_exam_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Exit Exam process failed: {e}")
            raise

    @allure.step("Confirm Contact page process")
    def confirm_contact_page_process(self):
        try:
            expected_url = self.test_urls["base_url"] + self.test_urls["paths"][28]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")

            self.wait_for_visible(ConfirmContactPageLocators.EMAIL_ADDRESS)
            email_value = self.page.get_attribute(ConfirmContactPageLocators.EMAIL_ADDRESS, "value")
            print(f"Email text: {email_value}")
            print(f"Expected email: {self.test_data['email']}")
            assert self.test_data["email"] in email_value

            self.wait_for_visible(ConfirmContactPageLocators.PHONE_NUMBER)
            phone_value = self.page.get_attribute(ConfirmContactPageLocators.PHONE_NUMBER, "value")
            cleaned_phone_value = clean_phone_number(phone_value)  # Clean the phone number from the page
            print(f"PHONE_NUMBER text: {cleaned_phone_value}")
            print(f"Expected PHONE_NUMBER: {self.test_data['phone_number']}")
            assert cleaned_phone_value == self.test_data["phone_number"]

            self.logger.info(f"Clicking Next button on URL {self.page.url}")
            self.click_with_retry(ConfirmContactPageLocators.NEXT_BUTTON, expected_url)

            screenshot_path = take_screenshot(self.page, "confirm_contact_passed")
            allure.attach.file(str(screenshot_path), name="confirm_contact_passed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Confirm Contact process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "confirm_contact_failed")
            allure.attach.file(str(screenshot_path), name="confirm_contact_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Confirm Contact process failed: {e}")
            raise

    @allure.step("Result Page process")
    def result_page_process(self):
        try:
            expected_url = self.test_urls["base_url"] + self.test_urls["paths"][29]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")

            self.logger.info(f"Clicking Next button on URL {self.page.url}")
            self.click_with_retry(ResultsPageLocators.NEXT_BUTTON, expected_url)
            screenshot_path = take_screenshot(self.page, "result_page_passed")
            allure.attach.file(str(screenshot_path), name="result_page_passed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Result Page process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "result_page_failed")
            allure.attach.file(str(screenshot_path), name="result_page_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Result Page process failed: {e}")
            raise

    @allure.step("College Plan process")
    def college_plan_process(self):
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][30], CollegePlanPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][31], CollegePlanPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][32], CollegePlanPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                # (self.test_urls["base_url"] + self.test_urls["paths"][33], CollegePlanPageLocators.NEXT_BUTTON,
                #  self.click_with_retry, "Click Next Button"),
            ]

            for step_index, (expected_url, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_url):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_url}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_url)

            self.click(CollegePlanPageLocators.NEXT_BUTTON)

            screenshot_path = take_screenshot(self.page, "college_plan_process_completed")
            allure.attach.file(str(screenshot_path), name="college_plan_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("College Plan process completed.")
        except Exception as e:
            screenshot_path = take_screenshot(self.page, "college_plan_process_failed")
            allure.attach.file(str(screenshot_path), name="college_plan_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"College Plan process failed: {e}")
            raise

    @allure.step("Decision PreBuy or No PreBuy")
    def decision_PreBuy_or_NoPreBuy(self, option=PREBUY):
        try:
            expected_url = self.test_urls["base_url"] + self.test_urls["paths"][34]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")
            if(option==True):
                self.logger.info(f"Clicking Start My Plan button on URL {self.page.url}")
                self.click(PreBuyOrNotPreBuyOptionsPageLocators.START_MY_PLAN)
                self.bridge_plan_checkout_process()
            else:
                self.logger.info(f"Clicking Continue with out a plan button on URL {self.page.url}")
                self.click(PreBuyOrNotPreBuyOptionsPageLocators.CONTINUE_WITH_OUT_A_PLAN)
                if(DECISION=="IMMEDIATE"):
                    self.ready_immediate_path()
                elif(DECISION=="SOON"):
                    self.ready_soon_path()
                elif(DECISION=="NOTYET"):
                    self.ready_not_yet_path()

        except Exception as e:
            screenshot_path = take_screenshot(self.page, "college_plan_process_failed")
            allure.attach.file(str(screenshot_path), name="college_plan_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"College Plan process failed: {e}")
            raise

    @allure.step("Bridge Plan Checkout Process")
    def bridge_plan_checkout_process(self):
        try:
            expected_url = self.test_urls["base_url"] + self.test_urls["paths"][35]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")

            self.logger.info(f"Verify the Name on card")
            name = self.page.get_attribute(PreBuyCheckoutPageLocators.NAME_ON_CARD, "value")
            full_name = self.test_data["first_name"]+" "+self.test_data["last_name"]
            print(f"Name on card: {name}")
            print(f"Expected name on card: {full_name}")
            assert full_name in name

            print(f"Card Number: {self.test_cards['card_number']}")
            self.enter_text_with_retry(PreBuyCheckoutPageLocators.CARD_NUMBER, self.test_cards["card_number"])
            self.enter_text_with_retry(PreBuyCheckoutPageLocators.EXPIRY, self.test_cards["expiry"])
            self.enter_text_with_retry(PreBuyCheckoutPageLocators.CVV, self.test_cards["cvv"])
            self.enter_text_with_retry(PreBuyCheckoutPageLocators.POSTAL_CODE, self.test_cards["postal_code"])

            self.logger.info(f"Verify the Email Address")
            email_address = self.page.get_attribute(PreBuyCheckoutPageLocators.EMAIL_ADDRESS, "value")
            email = self.test_data["email"]
            print(f"Email address: {email_address}")
            print(f"Expected email address: {email}")
            assert email_address in email

            self.click_with_retry(PreBuyCheckoutPageLocators.CHECKBOX, expected_url)
            self.click_with_retry(PreBuyCheckoutPageLocators.PAY_NOW, expected_url)
            time.sleep(25)

            self.logger.info(f"Verify the Bridge Plan Purchased Message")
            expected_congratulations_text = f"Congrats, {self.test_data['first_name']}!You’ve taken the first step toward building an RN Bridge Plan that fits your life."

            # Wait for the element to ensure it’s loaded
            self.page.wait_for_selector(PreBuyPurchasedPageLocators.CONGRATULATIONS_TEXT, state="visible")
            congratulations_text = self.page.text_content(PreBuyPurchasedPageLocators.CONGRATULATIONS_TEXT).strip()

            # Log raw strings for debugging
            print(f"Actual (repr): {repr(congratulations_text)}")
            print(f"Expected (repr): {repr(expected_congratulations_text)}")

            # Normalize apostrophes
            congratulations_text = congratulations_text.replace("'", "’")

            # Assert with stripped strings
            assert congratulations_text == expected_congratulations_text, f"Text mismatch: got '{congratulations_text}', expected '{expected_congratulations_text}'"

            screenshot_path = take_screenshot(self.page, "bridge_plan_checkout_process_completed")
            allure.attach.file(str(screenshot_path), name="bridge_plan_checkout_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Bridge Plan Checkout process completed.")

        except Exception as e:
            screenshot_path = take_screenshot(self.page, "bridge_plan_checkout_process_failed")
            allure.attach.file(str(screenshot_path), name="bridge_plan_checkout_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"Bridge Plan Checkout process failed: {e}")
            raise

    @allure.step("'Immediately. I'm ready to select a plan.' Process")
    def ready_immediate_path(self):
        try:
            expected_url = self.test_urls["base_url"] + self.test_urls["paths"][38]
            if not self.compare_current_url(expected_url):
                raise ValueError(f"Current URL {self.page.url} does not match {expected_url}")

            self.logger.info(f"Clicking 'Immediately. I'm ready to select a plan.' button on URL {self.page.url}")
            self.click_with_retry(ReadinessPageLocators.IMMEDIATELY, expected_url)
            self.logger.info(f"Clicking Next button on URL {self.page.url}")
            self.click_with_retry(ReadinessPageLocators.NEXT_BUTTON, expected_url)

            screenshot_path = take_screenshot(self.page, "ready_immediate_process_completed")
            allure.attach.file(str(screenshot_path), name="ready_immediate_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Ready Immediate process completed.")

        except Exception as e:
            screenshot_path = take_screenshot(self.page, "ready_immediate_process_failed")
            allure.attach.file(str(screenshot_path), name="ready_immediate_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"'Immediately. I'm ready to select a plan.' process failed: {e}")
            raise

    @allure.step("'Soon. I’m ready to discuss my RN goals.' Process")
    def ready_soon_path(self):
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][38], ReadinessPageLocators.SOON,
                 self.click_with_retry, "Clicking 'Soon. I’m ready to discuss my RN goals"),
                (self.test_urls["base_url"] + self.test_urls["paths"][38], ReadinessPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][41], ReadySoonThanksPageLocators.BLOG,
                 self.compare_element_href, "Verify Blog"),
                (self.test_urls["base_url"] + self.test_urls["paths"][41], ReadySoonThanksPageLocators.FAQS,
                 self.compare_element_href, "Verify FAQs"),
                (self.test_urls["base_url"] + self.test_urls["paths"][41], ReadySoonThanksPageLocators.NURSING_CARRIER_PATHWAY,
                 self.compare_element_href, "Verify Nursing Career Pathway")
            ]

            for step_index, (expected_value, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_value):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_value}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_value)

            screenshot_path = take_screenshot(self.page, "ready_soon_process_completed")
            allure.attach.file(str(screenshot_path), name="ready_soon_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("Ready Immediate process completed.")

        except Exception as e:
            screenshot_path = take_screenshot(self.page, "ready_soon_process_failed")
            allure.attach.file(str(screenshot_path), name="ready_soon_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"'Soon. I’m ready to discuss my RN goals.' process failed: {e}")
            raise

    @allure.step("'Not yet. I'd like more information.' Process")
    def ready_not_yet_path(self):
        try:
            steps = [
                (self.test_urls["base_url"] + self.test_urls["paths"][38], ReadinessPageLocators.NOT_YET,
                 self.click_with_retry, "Clicking 'Soon. I’m ready to discuss my RN goals"),
                (self.test_urls["base_url"] + self.test_urls["paths"][38], ReadinessPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][42], ReadyNotYetVideoPageLocators.NEXT_BUTTON,
                 self.click_with_retry, "Click Next Button"),
                (self.test_urls["base_url"] + self.test_urls["paths"][43], ReadyNotYetThanksPageLocators.BLOG,
                 self.compare_element_href, "Verify Blog"),
                (self.test_urls["base_url"] + self.test_urls["paths"][43], ReadyNotYetThanksPageLocators.FAQS,
                 self.compare_element_href, "Verify FAQs"),
                (self.test_urls["base_url"] + self.test_urls["paths"][43], ReadyNotYetThanksPageLocators.NURSING_CARRIER_PATHWAY,
                 self.compare_element_href, "Verify Nursing Career Pathway")
            ]

            for step_index, (expected_value, locator, action, description) in enumerate(steps, 1):
                if not self.compare_current_url(expected_value):
                    raise ValueError(
                        f"Step {step_index} ({description}): Current URL {self.page.url} does not match {expected_value}")
                self.logger.info(f"Step {step_index}: {description} on URL {self.page.url}")
                action(locator, expected_value)


            screenshot_path = take_screenshot(self.page, "ready_soon_process_completed")
            allure.attach.file(str(screenshot_path), name="ready_soon_process_completed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.info("'Not yet. I'd like more information.' process completed.")

        except Exception as e:
            screenshot_path = take_screenshot(self.page, "ready_soon_process_failed")
            allure.attach.file(str(screenshot_path), name="ready_soon_process_failed",
                               attachment_type=allure.attachment_type.PNG)
            self.logger.error(f"'Not yet. I'd like more information.' process failed: {e}")
            raise