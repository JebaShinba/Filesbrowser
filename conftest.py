import base64
import pytest
import os

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"screenshots/{item.name}.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

            # Save screenshot and encode it as Base64
            if driver.save_screenshot(screenshot_path):
                print(f"Screenshot saved at: {screenshot_path}")
                with open(screenshot_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

                # Add the Base64 image to the HTML report
                pytest_html = item.config.pluginmanager.getplugin('html')
                if pytest_html:
                    extra = getattr(report, 'extra', [])
                    img_html = f'<img src="data:image/png;base64,{encoded_string}" alt="screenshot" />'
                    extra.append(pytest_html.extras.html(img_html))
                    report.extra = extra
            else:
                print("Failed to save screenshot.")
