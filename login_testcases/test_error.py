import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from homeobjects.login import LoginPage
from configfile.config import get_db, get_users_collection  # Imports from config

@pytest.fixture(scope="module")
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, useful for CI/CD environments
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (recommended for headless mode on Windows)
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size to avoid potential issues with headless mode

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
    print("Browser closed.")

@pytest.fixture(scope="module")
def valid_users():
    # Fetch valid user credentials from MongoDB
    db = get_db()  # Establishes the database connection
    users_collection = get_users_collection()  # Gets the users collection

    # Retrieve only valid users
    users = list(users_collection.find({"is_valid": False}))
    print("Valid users fetched:", users)  # Debugging output

    if not users:
        pytest.fail("No valid users found in the database!")
    
    return users

@pytest.mark.parametrize("user_details", valid_users(), ids=lambda user: user.get("username", "Unknown user"))
def test_login_with_valid_users(setup_driver, user_details):
    required_keys = ["username", "password", "baseurl", "expected_error"]
    
    # Ensure all necessary keys are present
    if not all(key in user_details for key in required_keys):
        pytest.skip(f"Skipping login due to missing keys: {user_details}")
    
    username = user_details["username"]
    password = user_details["password"]
    base_url = user_details["baseurl"]
    expected_error = user_details["expected_error"]

    # Print the username and password being tested
    print(f"Testing login for Username: '{username}' with Password: '{password}'")

    # Navigate to the base URL
    driver = setup_driver
    try:
        driver.get(base_url)
        print("Navigated to:", base_url)
    except Exception as e:
        pytest.skip(f"Error navigating to base URL: {e}")

    # Instantiate the LoginPage object
    lg = LoginPage(driver)
    lg.setUsername(username)  # Enter the username
    lg.setPassword(password)  # Enter the corresponding password
    lg.clickLogin()
    actual_error = lg.actualError()
    
    # Assert that the actual error matches the expected error
    assert expected_error == actual_error, f"Failed for Username: '{username}' with Password: '{password}'"
