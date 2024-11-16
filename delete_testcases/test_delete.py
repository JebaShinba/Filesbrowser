from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
from homeobjects.test_login import LoginPage
from homeobjects.test_home import HomePage
from configfile.config import MongoClient  # Assuming MongoClient is correctly imported
import time

@pytest.fixture(scope="class")
def setup_class(request):
    """Setup Selenium WebDriver for the test class in headless mode."""
    options = Options()
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--no-sandbox")  # Required for some environments (e.g., Docker)
    options.add_argument("--disable-dev-shm-usage")  # For some environments with limited resources

    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is installed and on PATH
    driver.implicitly_wait(30)
    request.cls.driver = driver
    yield
    driver.quit()
    print("WebDriver instance closed.")

# Fixture for MongoDB client connection
@pytest.fixture(scope="module")
def mongo_client():
    """Set up MongoDB client connection."""
    client = MongoClient("mongodb://127.0.0.1:27017/")  # Update URI if necessary
    db = client["sampleupload"]  # Replace with your database name
    users_collection = db["users"]  # Replace with your collection name
    yield users_collection
    client.close()
    print("MongoDB client connection closed.")

@pytest.mark.usefixtures("setup_class")
class TestDelete:
    """Test class for delete functionality."""
    logged_in = False

    @pytest.fixture(autouse=True)
    def load_valid_files(self, mongo_client):
        """Load valid files for deletion from MongoDB."""
        valid_delete_files = list(mongo_client.find({"is_valid": True}))
        if not valid_delete_files:
            pytest.fail("No valid files found in the database!")
        self.valid_delete_files = valid_delete_files

    def test_delete_files(self):
        """Test case for deleting files."""
        for index, delete_details in enumerate(self.valid_delete_files):
            # Ensure required keys are present
            required_keys = {"folder_name", "file_name", "baseurl", "user_name", "password"}
            if not required_keys.issubset(delete_details):
                print(f"Skipping entry at index {index} due to missing keys: {delete_details.keys()}")
                continue

            # Extract details
            username = delete_details["user_name"]
            password = delete_details["password"]
            base_url = delete_details["baseurl"]
            folder_name = delete_details["folder_name"]
            file_name = delete_details["file_name"]

            # Navigate to the base URL
            try:
                self.driver.get(base_url)
                print(f"Navigated to: {base_url}")
            except Exception as e:
                print(f"Error navigating to {base_url}: {e}")
                continue

            # Login if not already logged in
            if not self.logged_in:
                try:
                    login_page = LoginPage(self.driver)
                    login_page.setUsername(username)
                    login_page.setPassword(password)
                    login_page.clickLogin()
                    self.logged_in = True
                    print(f"Login successful for user: {username}")
                except Exception as e:
                    print(f"Error during login for {username}: {e}")
                    continue

            # Delete the file
            try:
                home_page = HomePage(self.driver)
                home_page.clickMyFiles()
                print("Clicked My Files")
                home_page.selectFolder(folder_name)
                print(f"Folder selected: {folder_name}")
                home_page.selectFile(file_name)
                print(f"File selected: {file_name}")
                home_page.delete()
                home_page.confirmDelete()  # Assuming confirmDelete() is for confirmation
                print(f"File '{file_name}' in folder '{folder_name}' deleted successfully.")
            except Exception as e:
                print(f"Error deleting file '{file_name}' in folder '{folder_name}': {e}")
