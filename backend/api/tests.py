from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from datetime import datetime
import time

class CreateDPIFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        # Setting up Chrome WebDriver with options
        options = webdriver.ChromeOptions()
        # Uncomment the next line for headless mode
        # options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(5)
        
        # Create a test user in Django
        self.user = User.objects.create_user(username="admin_user", password="adminpassword123")
        
    def tearDown(self):
        # Close the browser after each test
        self.browser.quit()

    def test_create_dpi_form(self):
        try:
            # 1. Navigate to the login page
            self.browser.get("http://localhost:4200/login/")

            # Wait for the username input to be present
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            ).send_keys("admin_user")

            # Enter password and submit
            password_field = self.browser.find_element(By.ID, "password")
            password_field.send_keys("adminpassword123")

            # Locate the submit button and click it
            submit_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.submit-button"))
            )
            submit_button.click()

            # Verify login was successful
            WebDriverWait(self.browser, 10).until(
                EC.url_contains("/users/administratif")  
            )
             # 2. Click the "Ajouter DPI" button
            add_dpi_button = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "add-btn"))
            )
            add_dpi_button.click()

            # Verify navigation to the create-DPI page
            WebDriverWait(self.browser, 10).until(
                EC.url_contains("/users/administratif/create-dpi")
            )
            
            # Wait for the form to be present
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dpi-form"))
            )

            # 3. Fill out the form
            form_data = {
                "patient": "Billel_Moussous",
                "medecin_traitant": "Dr.Sarah_Ghecham",
                "nss": "123456789012345",  # 15 digits
                "date_naissance": "01012000",  # Format DDMMYYYY
                "adresse": "123 Rue Didouche Mourad, Alger",
                "telephone": "0123456789",  # 10 digits
                "mutuelle": "Mutuelle Générale",
                "personne_a_contacter": "Jhon Doe",
            }

            for field_id, value in form_data.items():
                element = self.browser.find_element(By.ID, field_id)
                if field_id == "date_naissance":
                    # Special formatting for the date field
                    formatted_date = datetime.strptime(value, "%d%m%Y").strftime("%Y-%m-%d")
                    element.send_keys(formatted_date)
                else:
                    element.send_keys(value)
                time.sleep(0.5)  

            # 4. Submit the form
            submit_button = self.browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
            self.browser.execute_script("arguments[0].scrollIntoView();", submit_button)
            submit_button.click()

            # 5. Check for the success message
            success_message = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "notification.success"))
            )
            self.assertIn("DPI", success_message.text)
            time.sleep(10)  
            

        except Exception as e:
            # Capture screenshot and print details for debugging
            self.browser.save_screenshot("error_screenshot.png")
            print(f"Current URL: {self.browser.current_url}")
            print(f"Page Source:\n{self.browser.page_source}")
            raise e

   