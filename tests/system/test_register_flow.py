import unittest
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app import create_app
from config import TestingConfig
from app.extensions import db
from app.models.user import User
from datetime import datetime, timezone

class RegisterFlowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[Setup] Starting Flask test server for register test...")

        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.driver = webdriver.Chrome(options=cls._chrome_options())
        cls.server_thread = Thread(target=cls.app.run, kwargs={"use_reloader": False})
        cls.server_thread.daemon = True
        cls.server_thread.start()
        cls.base_url = "http://localhost:5000"

    @classmethod
    def _chrome_options(cls):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        return options

    @classmethod
    def tearDownClass(cls):
        print("[Teardown] Closing browser and cleaning environment")
        cls.driver.quit()
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_register_new_user(self):
        print("\n[Test 5] Registering a new user")

        # Open registration page
        self.driver.get(f"{self.base_url}/register")

        # Fill in form fields
        self.driver.find_element(By.ID, "email").send_keys("newuser@example.com")
        self.driver.find_element(By.ID, "password").send_keys("testpass123")
        self.driver.find_element(By.ID, "role").send_keys("Support Worker")

        # Submit the form
        self.driver.find_element(By.NAME, "submit").click()

        # Check if redirected to the login page
        self.assertIn("/login", self.driver.current_url)

        # Check if the flash message contains a success notification
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Registration successful", body_text)

        print("[✓] Test 5 passed: User successfully registered and redirected to login.")
