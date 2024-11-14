import pytest
import os

# Define the screenshot directory
screenshot_dir = "screenshots"

# Create the screenshots directory if it doesn't exist
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Only add screenshot if the test failed
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("setup_driver", None)
        if driver:
            # Define the screenshot path relative to the HTML report
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)

            # Embed the screenshot in the HTML report
            extra = getattr(report, 'extra', [])
            pytest_html = item.config.pluginmanager.getplugin('html')
            if pytest_html:
                extra.append(pytest_html.extras.image(screenshot_path))
            report.extra = extra
