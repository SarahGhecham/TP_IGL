from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from api.models import Administratif


class CreateDPIFunctionalTest(LiveServerTestCase):
    """
    Selenium Functional Test for Create DPI View
    """

    def setUp(self):
        # Setup WebDriver with headless mode (optional for debugging)
        options = webdriver.ChromeOptions()
        # Uncomment the line below to run in headless mode
        # options.add_argument('--headless')  
        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(10)  # Adjust waiting time as needed

        # Create an admin user and assign necessary permissions
        self.admin_user = User.objects.create_user(username='admin_user', password='adminpassword123')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Create additional objects like 'Administratif' (adjust according to your model)
        Administratif.objects.create(user=self.admin_user)

    def tearDown(self):
        # Close the browser after test execution
        self.browser.quit()

    def test_create_dpi(self):
        """
        Test that admin can create a DPI via the form on the site.
        """
        try:
            # Step 1: Login as admin user
            self.browser.get(self.live_server_url + '/login/')
            username_field = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            username_field.send_keys('admin_user')

            password_field = self.browser.find_element(By.ID, 'password')
            password_field.send_keys('adminpassword123', Keys.RETURN)

            # Step 2: Navigate to Create DPI Page
            self.browser.get(self.live_server_url + '/users/administratif/create-dpi')

            # Step 3: Fill out the DPI form
            self.browser.find_element(By.ID, 'patient').send_keys('patient_user')
            self.browser.find_element(By.ID, 'medecin_traitant').send_keys('medecin_user')
            self.browser.find_element(By.ID, 'nss').send_keys('123456789')
            self.browser.find_element(By.ID, 'date_naissance').send_keys('2000-01-01')
            self.browser.find_element(By.ID, 'adresse').send_keys('123 Main St')
            self.browser.find_element(By.ID, 'telephone').send_keys('0123456789')
            self.browser.find_element(By.ID, 'mutuelle').send_keys('InsuranceXYZ')
            self.browser.find_element(By.ID, 'personne_a_contacter').send_keys('John Doe')

            # Step 4: Submit the form and verify success message
            self.browser.find_element(By.ID, 'submit-button').click()
            success_message = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'notification.success'))
            )
            self.assertIn('DPI successfully created', success_message.text)

        except Exception as e:
            # Log debugging information
            print(f"Error encountered: {e}")
            print(f"Current URL: {self.browser.current_url}")
            print(f"Page Source:\n{self.browser.page_source}")
            raise e
