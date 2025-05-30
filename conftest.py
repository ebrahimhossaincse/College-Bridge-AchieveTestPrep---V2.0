import pytest
import allure
from playwright.sync_api import sync_playwright

from config.base_config import BaseConfig
from utils.helpers import take_screenshot
import shutil
import os
import pytest

def clean_directory(directory):
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"❌ Failed to delete {file_path}. Reason: {e}")
    else:
        os.makedirs(directory)

def pytest_sessionstart(session):
    """Hook to clean up folders before test session starts."""
    clean_directory(BaseConfig.REPORT_DIR)
    clean_directory(BaseConfig.SCREENSHOT_DIR)
    clean_directory(BaseConfig.RECORD_VIDEO_DIR)
    clean_directory(BaseConfig.LOGS_DIR)
    print("✅ Cleaned reports/ , screenshots/ and video/ folders.")

def pytest_addoption(parser):
    parser.addoption(
        "--test-browser", action="store", default="chromium",
        help="Browser to use: chromium, firefox, or webkit"
    )
    parser.addoption(
        "--headless", action="store", default="False",
        help="Run browser in headless mode: True or False"
    )

@pytest.fixture(scope="session")
def browser(pytestconfig):
    browser_name = pytestconfig.getoption("--test-browser").lower()
    headless = pytestconfig.getoption("--headless").lower() == "true"

    with sync_playwright() as p:
        try:
            browser_type = getattr(p, browser_name)
        except AttributeError:
            raise ValueError(f"Unsupported browser: '{browser_name}'. Use chromium, firefox, or webkit.")

        browser = browser_type.launch(headless=headless)
        yield browser
        browser.close()

@pytest.fixture(scope="class")
def page(browser, request):
    BaseConfig.RECORD_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        record_video_dir=str(BaseConfig.RECORD_VIDEO_DIR),
        record_video_size={"width": 1920, "height": 1080}  # 👈 Set resolution here
    )
    context.clear_cookies()
    context.clear_permissions()
    page = context.new_page()
    request.cls.page = page
    yield page

    # Stop and save video
    video_path = page.video.path()

    # Attach video to Allure
    allure.attach.file(
        video_path,
        name=f"{request.node.name}_video",
        attachment_type=allure.attachment_type.MP4  # Only MP4 is supported
    )

    # Automatically take a screenshot after each test
    screenshot_path = take_screenshot(page, request.node.name)
    allure.attach.file(
        str(screenshot_path),
        name=f"{request.node.name}_screenshot",
        attachment_type=allure.attachment_type.PNG
    )
    context.close()
