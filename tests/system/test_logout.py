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
from werkzeug.security import generate_password_hash

class LogoutFlowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[Setup] Starting Flask test server for logout test...")

        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # Insert a Support Worker user
        cls.sw_password = "12345678"
        sw = User(
            email='swlogout@example.com',
            password_hash=generate_password_hash(cls.sw_password),
            role='Support Worker',
            full_name='Test SW',
            register_time=datetime.now(timezone.utc)
        )
        db.session.add(sw)
        db.session.commit()

        cls.sw_email = sw.email
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

    def test_logout_flow(self):
        print("\n[Test 4] Login and Logout Support Worker")

        # Login
        self.driver.get(f"{self.base_url}/login")
        self.driver.find_element(By.ID, "email").send_keys(self.sw_email)
        self.driver.find_element(By.ID, "password").send_keys(self.sw_password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

        # After redirecting to the dashboard, access the /logout route
        self.driver.get(f"{self.base_url}/logout")

        # Check if redirected back to the login page
        self.assertIn("/login", self.driver.current_url)
        print("[✓] Test 4 passed: Logout successful, redirected to login page.")
