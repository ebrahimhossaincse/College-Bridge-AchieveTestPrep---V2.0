import time

from utils.generate_random_test_data import fetch_fake_users, save_to_json
from utils.logger import setup_logger
from utils.helpers import highlight_element, take_screenshot
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import allure

class BasePage:
    def __init__(self, page):
        self.page = page
        self.logger = setup_logger(self.__class__.__name__)
        self.default_timeout = 60000  # milliseconds

    # ---------- Core Waits ----------
    def wait_for_visible(self, selector, timeout=None):
        try:
            self.logger.info(f"Waiting for {selector} to be visible.")
            self.page.locator(selector).wait_for(state="visible", timeout=timeout or self.default_timeout)
        except PlaywrightTimeoutError:
            self.logger.error(f"Element {selector} not visible after timeout.")
            raise

    def wait_for_attached(self, selector, timeout=None):
        self.logger.info(f"Waiting for {selector} to be attached to DOM.")
        self.page.locator(selector).wait_for(state="attached", timeout=timeout or self.default_timeout)

    def wait_for_enabled(self, selector, timeout=None):
        self.logger.info(f"Waiting for {selector} to be enabled.")
        self.page.locator(selector).wait_for(state="enabled", timeout=timeout or self.default_timeout)

    def wait_for_hidden(self, selector, timeout=None):
        self.logger.info(f"Waiting for {selector} to disappear.")
        self.page.locator(selector).wait_for(state="hidden", timeout=timeout or self.default_timeout)

    # ---------- Element Actions ----------
    def click(self, selector):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Clicking {selector}")
        self.page.click(selector)

    def double_click(self, selector):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Double-clicking {selector}")
        self.page.dblclick(selector)

    def enter_text(self, selector, text, clear_first=True):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Entering text '{text}' in {selector}")
        if clear_first:
            self.page.fill(selector, "")
        self.page.fill(selector, text)

    def append_text(self, selector, text):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Appending text '{text}' in {selector}")
        self.page.type(selector, text)

    def select_dropdown(self, selector, option_text):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Selecting option '{option_text}' in {selector}")
        self.page.select_option(selector, label=option_text)

    def get_text(self, selector):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        text = self.page.locator(selector).inner_text()
        self.logger.info(f"Text from {selector}: '{text}'")
        return text

    def get_attribute(self, selector, attribute_name):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        attr = self.page.locator(selector).get_attribute(attribute_name)
        self.logger.info(f"Attribute '{attribute_name}' of {selector}: '{attr}'")
        return attr

    def is_visible(self, selector):
        visible = self.page.locator(selector).is_visible()
        self.logger.info(f"Visibility of {selector}: {visible}")
        return visible

    def is_enabled(self, selector):
        enabled = self.page.locator(selector).is_enabled()
        self.logger.info(f"Enabled state of {selector}: {enabled}")
        return enabled

    def is_checked(self, selector):
        checked = self.page.locator(selector).is_checked()
        self.logger.info(f"Checked state of {selector}: {checked}")
        return checked

    # ---------- User-Like Actions ----------
    def hover(self, selector):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Hovering over {selector}")
        self.page.hover(selector)

    def scroll_into_view(self, selector):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Scrolling into view {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def take_element_screenshot(self, selector, path):
        self.wait_for_visible(selector)
        highlight_element(self.page, selector)
        self.logger.info(f"Taking screenshot of {selector}")
        self.page.locator(selector).screenshot(path=path)

    # ---------- Assertions ----------
    def assert_text(self, selector, expected_text):
        actual_text = self.get_text(selector)
        highlight_element(self.page, selector)
        assert actual_text == expected_text, f"Expected: '{expected_text}', Got: '{actual_text}'"

    def assert_element_visible(self, selector):
        highlight_element(self.page, selector)
        assert self.is_visible(selector), f"Element {selector} should be visible"

    def assert_element_not_visible(self, selector):
        highlight_element(self.page, selector)
        assert not self.is_visible(selector), f"Element {selector} should not be visible"

    # ---------- Utility ----------
    def reload_page(self):
        self.logger.info("Reloading the page.")
        self.page.reload()

    def go_to(self, url):
        self.logger.info(f"Navigating to: {url}")
        self.page.goto(url, wait_until="load")

    def execute_script(self, script: str):
        self.logger.info(f"Executing JavaScript: {script}")
        return self.page.evaluate(script)

    def get_current_url(self):
        url = self.page.url
        self.logger.info(f"Retrieved current URL: '{url}'")
        return url

    def compare_current_url(self, expected_url, timeout=5000, retries=5):
        """Compare current URL with expected URL, waiting and retrying if needed."""
        attempt = 1
        while attempt <= retries:
            try:
                self.logger.debug(f"Attempt {attempt}/{retries}: Waiting for URL {expected_url}")
                self.page.wait_for_url(expected_url, timeout=timeout)
                self.logger.info(f"URL matched: {self.page.url}")
                return True
            except Exception as e:
                self.logger.warning(
                    f"Attempt {attempt}/{retries}: Current URL {self.page.url} does not match {expected_url}. Error: {e}")
                if attempt == retries:
                    self.logger.error(f"URL check failed after {retries} attempts")
                    return False
                attempt += 1
        return False

    def compare_element_href(self, selector, expected_href, timeout=5000, retries=5):
        """Compare element's href attribute with expected href, waiting and retrying if needed."""
        attempt = 1
        while attempt <= retries:
            try:
                self.logger.debug(
                    f"Attempt {attempt}/{retries}: Waiting for href {expected_href} on element {selector}")
                element = self.page.wait_for_selector(selector, timeout=timeout)
                actual_href = element.get_attribute('href')
                if actual_href == expected_href:
                    self.logger.info(f"Href matched: {actual_href}")
                    return True
                else:
                    raise Exception(f"Href mismatch: got {actual_href}, expected {expected_href}")
            except Exception as e:
                self.logger.warning(
                    f"Attempt {attempt}/{retries}: Href check failed for {selector}. Error: {e}")
                if attempt == retries:
                    self.logger.error(f"Href check failed after {retries} attempts")
                    return False
                attempt += 1
        return False

    def click_with_retry(self, locator, expected_url, retries=5):
        """Click an element with retries, handling same-page scenarios."""
        initial_url = self.page.url
        for attempt in range(retries):
            try:
                element = self.page.locator(locator)
                element.scroll_into_view_if_needed()
                element.wait_for(state="visible", timeout=5000)
                is_enabled = element.is_enabled()
                self.logger.info(f"Attempt {attempt + 1}: Clicking locator {locator}, enabled={is_enabled}")
                if attempt < retries - 1:
                    highlight_element(self.page, locator)
                    element.click()
                else:
                    self.page.evaluate("el => el.click()", element)
                self.page.wait_for_timeout(1500)
                if self.page.url != initial_url:
                    self.logger.info(f"Click successful on attempt {attempt + 1}, URL changed to {self.page.url}")
                    return
                if self.is_content_updated(locator):
                    self.logger.info(f"Click successful on attempt {attempt + 1}, content updated without URL change")
                    return
                self.logger.warning(f"Attempt {attempt + 1}: URL did not change after clicking {locator}, retrying...")
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for locator {locator}: {e}")
            if attempt == retries - 1:
                raise ValueError(f"Failed to navigate or update content after {retries} attempts on locator {locator}")
            self.page.wait_for_timeout(1000)

    def is_content_updated(self, locator, timeout=2000):
        """Check if page content updated (e.g., new element appeared)."""
        try:
            self.page.wait_for_selector(locator, state="visible", timeout=timeout)
            return True
        except:
            return False

    def select_dropdown_with_retry(self, locator, value, retries=5):
        """Select a dropdown option with retries."""
        last_exception = None

        for attempt in range(retries):
            try:
                # Always get a fresh reference to the element
                element = self.page.locator(locator)

                # Scroll and wait with more robust conditions
                element.scroll_into_view_if_needed()
                # element.wait_for(state="visible", timeout=10000)
                # element.wait_for(state="enabled", timeout=5000)

                self.logger.info(f"Attempt {attempt + 1}: Selecting {value} in dropdown {locator}")
                highlight_element(self.page, locator)

                # More specific selection approach
                element.select_option(value, timeout=5000)

                # Optional: Verify selection was successful
                self.page.wait_for_timeout(1000)  # Small delay for UI update
                return
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} failed for dropdown {locator}: {str(e)}")
                if attempt < retries - 1:
                    self.logger.info("Waiting before retry...")
                    self.page.wait_for_timeout(2000)  # Longer wait between retries

        raise ValueError(
            f"Failed to select '{value}' in dropdown {locator} after {retries} attempts. "
            f"Last error: {str(last_exception)}"
        )

    def enter_text_with_retry(self, locator, value, retries=5):
        """Enter text into a field with retries."""
        for attempt in range(retries):
            try:
                element = self.page.locator(locator)
                element.scroll_into_view_if_needed()
                element.wait_for(state="visible", timeout=5000)
                self.logger.info(f"Attempt {attempt + 1}: Entering {value} in field {locator}")
                highlight_element(self.page, locator)
                element.fill(value)
                self.page.wait_for_timeout(1000)
                return
            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for field {locator}: {e}")
                if attempt == retries - 1:
                    raise ValueError(f"Failed to enter {value} in field {locator} after {retries} attempts")
                self.page.wait_for_timeout(1000)

    def get_text_with_retry(self, locator, expected_text=None, expected_url=None, retries=5, timeout=1000):

        for attempt in range(retries):
            try:
                # First verify URL if expected_url was provided
                if expected_url is not None:
                    current_url = self.page.url
                    if current_url != expected_url:
                        self.logger.warning(
                            f"Attempt {attempt + 1}: URL mismatch\n"
                            f"Expected: {expected_url}\n"
                            f"Actual: {current_url}"
                        )
                        if attempt == retries - 1:
                            raise ValueError(f"URL never matched expected URL after {retries} attempts\n"
                                             f"Expected: {expected_url}\nLast seen: {current_url}")
                        self.page.wait_for_timeout(timeout)
                        continue  # Skip text verification if URL is wrong

                # Only proceed to text verification if URL is correct (or not checked)
                element = self.page.locator(locator)
                element.scroll_into_view_if_needed()
                element.wait_for(state="visible", timeout=5000)

                # Highlight the element (except on last attempt)
                if attempt < retries - 1:
                    highlight_element(self.page, locator)

                # Get the text content
                text = element.text_content().strip()

                # Verify text content if expected_text was provided
                if expected_text is not None and expected_text not in text:
                    self.logger.warning(
                        f"Attempt {attempt + 1}: Text mismatch\n"
                        f"Expected to contain: {expected_text}\n"
                        f"Actual text: {text}"
                    )
                    raise ValueError("Text content mismatch")  # Will trigger retry

                # If we got here, all verifications passed
                self.logger.info(
                    f"Verifications passed on attempt {attempt + 1}\n"
                    f"URL: {self.page.url}\n"
                    f"Text: {text}"
                )
                return text

            except Exception as e:
                self.logger.warning(f"Attempt {attempt + 1} failed for locator {locator}: {str(e)}")
                if attempt == retries - 1:
                    raise ValueError(f"Failed after {retries} attempts on locator {locator}\n"
                                     f"Last error: {str(e)}")

            self.page.wait_for_timeout(timeout)