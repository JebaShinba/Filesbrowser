import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from homeobjects.test_login import LoginPage
from pymongo import MongoClient  # Assuming MongoClient is defined in config

@pytest.fixture(scope="module")
def mongo_client():
    """
    Fixture to initialize MongoDB client and fetch valid users.
    """
    client = MongoClient("mongodb://127.0.0.1:27017/")  # Update this URI as necessary
    db = client["sampleupload"]  # Use your actual database name
    users_collection = db["users"]  # Use your actual collection name
    valid_users = list(users_collection.find({"is_valid": True}))
    
    if not valid_users:
        pytest.fail("No valid users found in the database!")
    
    return valid_users, client

@pytest.fixture(scope="module")
def webdriver_instance():
    """
    Fixture to set up the Selenium WebDriver with necessary options.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    
    yield driver  # This will be used in the tests
    
    driver.quit()  # Close the browser after the test is done

def test_login_with_valid_users(mongo_client, webdriver_instance):
    """
    Test login with valid users fetched from MongoDB.
    """
    valid_users, _ = mongo_client
    driver = webdriver_instance

    for index, user_details in enumerate(valid_users):
        with pytest.subtests.test(user_index=index):
            required_keys = ["username", "password", "baseurl"]
            
            # Ensure all necessary keys are present
            if not all(key in user_details for key in required_keys):
                print("Skipping login due to missing keys:", user_details)
                continue  # Skip to the next user if keys are missing

            username = user_details["username"]
            password = user_details["password"]
            base_url = user_details["baseurl"]

            # Print the username and password being tested
            print(f"Testing login for Username: '{username}' with Password: '{password}'")

            # Navigate to the base URL
            try:
                driver.get(base_url)
                print("Navigated to:", base_url)
            except Exception as e:
                print("Error navigating to base URL:", e)
                continue  # Skip to the next user if navigation fails

            # Instantiate the LoginPage object
            lg = LoginPage(driver)
            lg.setUsername(username)  # Enter the username
            lg.setPassword(password)  # Enter the corresponding password
            lg.clickLogin()

@pytest.fixture(scope="module", autouse=True)
def cleanup(mongo_client):
    """
    Cleanup MongoDB client after the test.
    """
    _, client = mongo_client
    yield
    client.close()  # Close the MongoDB client after the tests are done
    print("MongoDB client connection closed.")

if __name__ == '__main__':
    pytest.main()
