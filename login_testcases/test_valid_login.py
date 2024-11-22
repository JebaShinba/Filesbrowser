from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from homeobjects.test_login import LoginPage
from configfile.config import MongoClient  # Assuming MongoClient is defined in config
import time
import os


@pytest.fixture(scope="module")
def mongo_client():
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["sampleupload"]
    users_collection = db["users"]
    yield users_collection
    client.close()
    print("MongoDB client connection closed.")


@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Remove this line for visual debugging
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Check for chromedriver path or use default
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "chromedriver")
    try:
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    except WebDriverException as e:
        pytest.fail(f"WebDriverException: {e}. Ensure 'chromedriver' is installed and in PATH.")
        return

    driver.implicitly_wait(5)
    yield driver
    driver.quit()
    print("Browser closed.")


def test_login_with_valid_users(driver, mongo_client):
    valid_users = list(mongo_client.find({"is_valid": True}))
    assert valid_users, "No valid users found in the database!"

    for index, user_details in enumerate(valid_users):
        required_keys = ["username", "password", "baseurl"]

        if not all(key in user_details for key in required_keys):
            pytest.skip(f"Skipping login due to missing keys in user: {user_details}")
            continue

        username = user_details["username"]
        password = user_details["password"]
        base_url = user_details["baseurl"]

        print(f"Testing login for Username: '{username}' with Password: '{password}'")

        # Navigate to the base URL
        try:
            driver.get(base_url)
            print("Navigated to:", base_url)
        except Exception as e:
            pytest.fail(f"Error navigating to base URL: {e}")
            continue

        # Perform login
        login_page = LoginPage(driver)
        login_page.setUsername(username)
        login_page.setPassword(password)
        login_page.clickLogin()

        time.sleep(2)  # Short delay to allow for any animations, if needed
        
        try:
            # Verify successful login
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Logout')]"))
            )
            print(f"Login successful for user: {username}")
        except TimeoutException:
            # Capture and log page source for debugging
            print(f"Login failed for user: {username}")
            print("Page source at the time of failure:")
            print(driver.page_source)
            pytest.fail(f"Timeout while waiting for successful login confirmation for user: {username}")
