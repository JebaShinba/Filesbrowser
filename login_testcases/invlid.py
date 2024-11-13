import pytest
from selenium import webdriver
from homeobjects.login import LoginPage
from configfile.config import get_db, get_users_collection  # Imports from config


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
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
    valid_users = list(users_collection.find({"is_valid": False}))
    
    print("Valid users fetched:", valid_users)  # Debugging output

    if not valid_users:
        raise Exception("No valid users found in the database!")

    return valid_users


@pytest.mark.parametrize("user_details", valid_users())
def test_login_with_valid_users(driver, user_details):
    required_keys = ["username", "password", "baseurl", "expected_error"]
    
    # Ensure all necessary keys are present
    if not all(key in user_details for key in required_keys):
        print("Skipping login due to missing keys:", user_details)
        pytest.skip("Missing required user details")

    username = user_details["username"]
    password = user_details["password"]
    base_url = user_details["baseurl"]
    expected_error = user_details["expected_error"]

    # Print the username and password being tested
    print(f"Testing login for Username: '{username}' with Password: '{password}'")

    # Navigate to the base URL
    try:
        driver.get(base_url)
        print("Navigated to:", base_url)
    except Exception as e:
        print("Error navigating to base URL:", e)
        pytest.skip(f"Navigation to base URL failed: {e}")

    # Instantiate the LoginPage object
    lg = LoginPage(driver)
    lg.setUsername(username)  # Enter the username
    lg.setPassword(password)  # Enter the corresponding password
    lg.clickLogin()
    actual_error = lg.actualError()   
    
    # Assert that the actual error matches the expected error
    assert actual_error == expected_error, f"Failed for Username: '{username}' with Password: '{password}'"
