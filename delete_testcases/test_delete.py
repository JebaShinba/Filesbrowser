import pytest
from selenium import webdriver
from samplewebsite.homeobjects.login import LoginPage
from samplewebsite.homeobjects.home import HomePage
from samplewebsite.configfile.config import get_db, get_files_collection

@pytest.fixture(scope="class")
def setup_class(request):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    request.cls.driver = driver

    # Connect to MongoDB and fetch valid delete files
    db = get_db()
    files_collection = get_files_collection()
    valid_delete_files = list(files_collection.find({"is_valid": True}))

    if not valid_delete_files:
        pytest.fail("No valid files found in the database!")

    request.cls.valid_delete_files = valid_delete_files
    yield
    driver.quit()

@pytest.mark.usefixtures("setup_class")
class TestDelete:
    logged_in = False

    def test_delete_files(self):
        for index, delete_details in enumerate(self.valid_delete_files):
            required_keys = {"folder_name", "file_name", "baseurl", "user_name", "password",  }
            if not required_keys.issubset(delete_details):
                print(f"Skipping entry at index {index} due to missing keys.")
                continue

            username = delete_details["user_name"]
            password = delete_details["password"]
            base_url = delete_details["baseurl"]
            folder_name = delete_details["folder_name"]
            file_name = delete_details["file_name"]

            # Navigate to the base URL
            try:
                self.driver.get(base_url)
                print("Navigated to:", base_url)
            except Exception as e:
                print("Error navigating to base URL:", e)
                continue

            # Login if not already logged in
            lg = LoginPage(self.driver)
            if not self.logged_in:
                try:
                    lg.setUsername(username)
                    lg.setPassword(password)
                    lg.clickLogin()
                    self.logged_in = True
                    print(f"Login attempted for user: {username}")
                except Exception as e:
                    print(f"Error during login for {username}: {e}")
                    continue

            # Delete the file
            hp = HomePage(self.driver)
            hp.clickMyfiles()
            print("Clicked My Files")
            hp.selectFolder(folder_name)
            print("Folder selected")
            hp.selectFile(file_name)
            hp.delete()
            hp.delete1()
