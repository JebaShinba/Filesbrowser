# conftest.py
import pytest
from selenium import webdriver
import os

# Ensure the screenshots folder exists
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

@pytest.fixture
def setup_driver():
    driver = webdriver.Chrome()  # or use Firefox, etc.
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook is used to capture test reports and take a screenshot on failure
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        try:
            # Access the WebDriver instance from the test
            driver = item.funcargs['setup_driver']
            # Define screenshot file path
            screenshot_path = f"screenshots/{item.name}.png"
            # Save the screenshot
            driver.save_screenshot(screenshot_path)
            # Attach the screenshot to the HTML report
            if screenshot_path:
                html = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:600px;height:auto;" onclick="window.open(this.src)" /></div>'
                report.extra = getattr(report, "extra", []) + [pytest_html.extras.html(html)]
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

def pytest_configure(config):
    # Add 'pytest-html' extras if it's installed
    global pytest_html
    pytest_html = config.pluginmanager.getplugin('html')
