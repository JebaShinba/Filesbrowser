from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
#storefiles_button_xpath = "//li[@role='button' and @aria-label='storefiles' and @aria-selected='false' and @data-url='/files/storefiles/']"
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging



class HomePage:
    def __init__(self, driver):
        # Initialize the driver instance for this page
        self.driver = driver

    

    def clickMyfiles(self):
        # Wait for "My files" to be located and click it
        myfiles = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[text()='My files']"))
        )
        myfiles.click()

    def selectFolder(self, folder_name):
        # Wait for the specified folder to be located
        select_folder = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//p[contains(@class, 'name') and text()='{folder_name}']"))
        )
        
        # Create an ActionChains object and perform a double-click on the folder
        actions = ActionChains(self.driver)
        actions.double_click(select_folder).perform()
    # def selectFolder(self, folder_name):
    #     logging.info("Attempting to locate and select folder: %s", folder_name)
    #     try:
    #         # Wait for the specified folder element to become visible
    #         select_folder = WebDriverWait(self.driver, 15).until(
    #             EC.visibility_of_element_located((By.XPATH, f"//p[contains(@class, 'name') and text()='{folder_name}']"))
    #         )
    #         logging.info("Folder '%s' located. Attempting double-click.", folder_name)

    #         # Perform a double-click on the folder
    #         actions = ActionChains(self.driver)
    #         actions.double_click(select_folder).perform()
    #         logging.info("Double-clicked on the folder: %s", folder_name)
            
    #     except TimeoutException:
    #         logging.error("TimeoutException: Unable to locate the folder named '%s' within the specified timeout.", folder_name)
    #         raise

    def selectFile(self, file_name):
        # Wait for the specified file to be located and click it
        select_file = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[@class='item' and @aria-label='{file_name}']"))
        )
        select_file.click()

        ##move details

    def forwardicon(self):
        forward_icon = WebDriverWait(self.driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//i[@class='material-icons' and text()='forward']"))
        )
        forward_icon.click()

    def folderclick(self):
            try:
                folder_button = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//li[@role='button' and @aria-label='..' and @aria-selected='false' and @data-url='/files/']"))
                )
                actions = ActionChains(self.driver)
                actions.double_click(folder_button).perform()
                print("Double-clicked on the folder button.")
            except Exception as e:
                print("Error in folderclick:", e)

    def folderSelected(self, folder_name1):
        storefiles_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f"//p[text()='{folder_name1}']"))
        )
        storefiles_button.click()
    def selectfile(self, folder_name1):
        try:
            # Wait until the store_files element is visible
            store_files_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, f"//li[@role='button' and @aria-label='{folder_name1}']"))
            )
            print("store_files is visible")

            # Attempt to click the element directly without JavaScript
            store_files_element.click()
            print("Clicked on store_files")

        except TimeoutException:
            print("Timed out waiting for store_files to become visible.")
        except Exception as e:
            print(f"Error during clicking store_files: {e}")



    def movebutton(self):
        move_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Move']"))
        )
        move_button.click()
        print("Clicked on move button")

    ##delete details

    def delete(self):
        # Wait for the delete icon to be located and click it
        delete_icon = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//i[contains(@class, 'material-icons') and text()='delete']"))
        )
        delete_icon.click()

    def delete1(self):
        # Wait for the confirm delete button to be located and click it
        confirm_delete_button = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='focus-prompt' and @aria-label='Delete']"))
        )
        confirm_delete_button.click()



    def download(self):
        # Wait for the confirm delete button to be located and click it
        download_icon = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//i[@class='material-icons' and contains(text(), 'file_download')]"))
        )
        download_icon.click()

        # copy

    def copy(self):
        # Wait for the confirm delete button to be located and click it
        copy_icon = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//i[text()='content_copy']"))
        )
        copy_icon.click()


    def click_copy_button(self):
        try:
            # Wait for the Copy button to be visible and clickable
            copy_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@id='focus-prompt' and @aria-label='Copy']"))
            )
            print("Copy button is visible and clickable.")

            # Attempt a direct click
            copy_button.click()
            print("Successfully clicked on the Copy button directly.")

        except Exception as e:
            print(f"Direct click failed, attempting JavaScript click due to: {e}")

            # Use JavaScript click as a fallback
            try:
                self.driver.execute_script("arguments[0].click();", copy_button)
                print("Successfully clicked on the Copy button using JavaScript.")
            except Exception as js_e:
                print(f"JavaScript click also failed: {js_e}")

        except TimeoutException:
            print("Timed out waiting for the Copy button to become clickable.")




    def multiicon(self):
        # Wait for the confirm delete button to be located and click it
        multi_icon = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//i[@class='material-icons' and text()='check_circle']"))
        )
        multi_icon.click()

    def zipbutton(self):
        # Wait until the "zip" button is visible and clickable, then click
        zip_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='zip']"))
        )
        zip_button.click()
        print("Zip button clicked")

    def tarbutton(self):
        # Wait until the "zip" button is visible and clickable, then click
        tar_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='tar']"))
        )
        tar_button.click()
        print("Zip button clicked")


#     def clickLogout(self):
#         # Find the logout button and click on it
#         try:
#             logout_button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, "//i[@class='q-icon notranslate material-icons' and text()='logout']"))
#             )
#             logout_button.click()
#         except Exception as e:
#             print(f"Error clicking logout: {e}")

#     # correctly run two cases
    
#     # def clickHome(self):
#     #     home_icon = WebDriverWait(self.driver, 10).until(
#     #         EC.visibility_of_element_located((By.XPATH, "//i[contains(@class, 'q-tree__arrow')]"))
#     #     )
#     #     home_icon.click()

#     def clickHome(self):
#         home_icon = WebDriverWait(self.driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, "//i[contains(@class, 'q-icon') and contains(@class, 'material-icons') and contains(@class, 'q-tree__arrow')]"))
#         )
#         home_icon.click()

#     def selectFolder(self):
#         select_folder = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//div[text()='new folder']"))
#         )
#         select_folder.click()

#     def clicknewFolderButton(self):
#         new_folder_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//span[text()='New Folder']"))
#         )
#         new_folder_button.click()

#     def clearButton(self):
#         clear_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//i[@class='q-icon notranslate material-icons q-field__focusable-action' and @aria-label='Clear']"))
#         )
#         clear_button.click()

#     def clickTab1(self,foldername):
#         new_folder_name = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='/new folder']"))
#         )
#         new_folder_name.click()
#         new_folder_name.send_keys(foldername)

#     def clickTab(self,foldername):
#         new_folder_name = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='/new folder']"))
#         )
#         new_folder_name.click()
#         new_folder_name.send_keys(foldername)

#     def createButton(self):
#         create_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'block') and text()='Create']"))
#         )
#         create_button.click()

#     def actual_erro(self):
#         return self.driver.find_element(By.XPATH, "//div[@role='alert' and text()='Empty string (or) spaces not allowed']").text
    
#     def cancelButton1(self):
#         cancel_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//i[@class='q-icon notranslate material-icons' and @aria-hidden='true' and @role='img' and text()='close']"))
#         )
#         cancel_button.click()
#     # correctly run cancel button in two cases

#     def cancelButton(self):
#         cancel_button = WebDriverWait(self.driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[@class='q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle text-primary q-btn--actionable q-focusable q-hoverable q-btn--dense']//i[@role='img' and text()='close']"))
#         )
#         cancel_button.click()

#     # def cancelButton(self):
#     #     cancel_button = WebDriverWait(self.driver, 10).until(
#     #         EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'q-btn__content') and contains(@class, 'text-center')]"))
#     #     )
#     #     cancel_button.click()


#     # def cancelButton(self):
#     #     try:
#     #         # Wait until the cancel button is clickable
#     #         cancel_button = WebDriverWait(self.driver, 10).until(
#     #             EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'q-icon') and contains(@class, 'material-icons') and @aria-hidden='true']"))
#     #         )
#     #         # Attempt to click the button
#     #         cancel_button.click()
#     #         print("Cancel button clicked successfully.")
#     #     except Exception as e:
#     #         print(f"Failed to click cancel button using regular click: {e}")
#     #         # Try to click using JavaScript as a fallback
#     #         self.driver.execute_script("arguments[0].click();", cancel_button)
#     #         print("Cancel button clicked using JavaScript.")

#     # def clearButton(self):
#     #     clear_button = WebDriverWait(self.driver, 10).until(
#     #         EC.element_to_be_clickable((By.XPATH, "//i[@class='q-icon notranslate material-icons q-field__focusable-action' and @aria-hidden='false' and @role='button' and @tabindex='0' and @aria-label='Clear' and text()='cancel']"))
#     #     )
#     #     clear_button.click()

# # In your HomePage class
#     def clearButton(self):

#             try:
#                 # Define the XPath for the clear button
#                 # clear_button_xpath = "//i[@class='q-icon notranslate material-icons q-field__focusable-action' and @aria-label='Clear']"
#                 clear_button_xpath = "//i[text()='cancel']"
#                 # Wait for the button to be clickable and then click it
#                 clear_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, clear_button_xpath)))
#                 clear_button.click()
#                 print("Clear button clicked successfully.")

#             except NoSuchElementException:
#                 print("Clear button not found.")
#             except Exception as e:
#                 print(f"An error occurred while clicking the Clear button: {e}")






    

    

    


