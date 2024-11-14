import pytest
import os

# Ensure the screenshots directory exists
screenshot_dir = os.path.abspath("screenshots")
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)

# Hook for adding additional information in the HTML report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Only add screenshot if the test failed
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("setup_driver", None)
        if driver:
            # Define absolute screenshot path
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
            driver.save_screenshot(screenshot_path)
            # Embed the screenshot in the HTML report
            pytest_html = item.config.pluginmanager.getplugin('html')
            extra = getattr(report, 'extra', [])
            extra.append(pytest_html.extras.image(screenshot_path))
            report.extra = extra
