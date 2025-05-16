from utils.logger import setup_logger
from utils.helpers import highlight_element
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

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
