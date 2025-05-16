import pytest
import allure
from playwright.sync_api import sync_playwright
from config.base_config import BaseConfig
from utils.helpers import take_screenshot

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = getattr(p, BaseConfig.BROWSER)
        browser = browser_type.launch(headless=BaseConfig.HEADLESS)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser, request):
    context = browser.new_context()
    page = context.new_page()
    yield page
    screenshot_path = take_screenshot(page, request.node.name)
    allure.attach.file(
        str(screenshot_path),
        name=f"{request.node.name}_screenshot",
        attachment_type=allure.attachment_type.PNG
    )
    context.close()
