import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from homeobjects.test_login import LoginPage
from configfile.config import MongoClient
import logging

# Set up logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# MongoDB setup functions
def get_db():
    """Set up MongoDB connection."""
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
    return client["sampleupload"]

def get_users_collection():
    """Get the user collection."""
    db = get_db()
    return db["users"]  # Replace with the actual collection name

@pytest.fixture(scope="class")
def setup_driver():
    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional but recommended for headless)
    options.add_argument("--no-sandbox")  # Disable the sandbox (necessary for some CI environments)

    # Initialize the WebDriver with the headless options
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
    logger.info("Browser closed.")

@pytest.fixture(scope="class")
def invalid_users():
    """Fixture to fetch invalid users from the database."""
    db = get_db()
    cls_user_collection = get_users_collection()

    logger.info(f"Database connected: {db}")
    logger.info(f"Connected to user collection: {cls_user_collection}")

    # Fetch users with invalid details
    invalid_user_details = list(cls_user_collection.find({"is_valid": False}))
    logger.info(f"Invalid user details fetched: {invalid_user_details}")

    if not invalid_user_details:
        raise Exception("No invalid user details found in the database!")

    return invalid_user_details  # Return the invalid users to be used in the test

@pytest.mark.usefixtures("setup_driver")
class TestValidLogin:
    def test_login_with_invalid_users(self, setup_driver, invalid_users):
        # Debugging: Check if invalid_users is being passed correctly
        logger.info(f"Invalid users fetched: {invalid_users}")
        
        # Iterate over invalid users and perform login
        for index, user_details in enumerate(invalid_users):
            logger.debug(f"Index: {index}, User details: {user_details}")

            required_keys = ["username", "password", "baseurl", "expected_error"]

            # Ensure all necessary keys are present
            if not all(key in user_details for key in required_keys):
                logger.warning(f"Skipping login due to missing keys: {user_details}")
                pytest.skip(f"Skipping due to missing keys: {user_details}")

            username = user_details["username"]
            password = user_details["password"]
            base_url = user_details["baseurl"]
            expected_error = user_details["expected_error"]

            logger.info(f"Testing login for Username: '{username}' with Password: '{password}', expected error: '{expected_error}'")

            # Handle empty username or password case
            if not username or not password:
                logger.error(f"Empty username or password found for user details: {user_details}")
                expected_error = "Wrong credentials"  # Adjust expected error as needed

            # Navigate to the base URL
            try:
                setup_driver.get(base_url)
                logger.info(f"Navigated to: {base_url}")
            except Exception as e:
                logger.error(f"Error navigating to base URL: {e}")
                pytest.skip(f"Skipping due to navigation error: {e}")

            # Instantiate the LoginPage object and attempt login
            lg = LoginPage(setup_driver)
            lg.setUsername(username)  # Enter the username
            lg.setPassword(password)  # Enter the corresponding password
            lg.clickLogin()
            actualerror = lg.actualError()

            # Assert that the actual error matches the expected error
            assert expected_error == actualerror, (
                f"Failed for Username: '{username}' with Password: '{password}'. "
                f"Expected error: '{expected_error}', but got: '{actualerror}'"
            )
