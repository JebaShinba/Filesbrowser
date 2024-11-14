import pytest
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute the test and get the result
    outcome = yield
    result = outcome.get_result()
    
    # Check if the test failed at the call stage
    if result.when == 'call' and result.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            # Ensure the screenshots directory exists
            screenshots_dir = "screenshots"
            os.makedirs(screenshots_dir, exist_ok=True)
            print(f"Created screenshots directory: {screenshots_dir}")
            
            # Define the screenshot path
            screenshot_path = f"{screenshots_dir}/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Saved screenshot for failed test '{item.name}' at {screenshot_path}")
            
            # Attach screenshot to the HTML report
            pytest_html = item.config.pluginmanager.getplugin('html')
            if pytest_html:
                extra = getattr(result, 'extra', [])
                extra.append(pytest_html.extras.image(screenshot_path))
                result.extra = extra
                print(f"Attached screenshot to HTML report for test '{item.name}'")
