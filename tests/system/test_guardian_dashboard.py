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

class GuardianDashboardTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[Setup] Starting Flask test server and initializing database")

        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        guardian = User(
            email='guardian@outlook.com',
            password_hash='scrypt:32768:8:1$KzGvlM5DMSXLhZ0J$be26c27c361359bca2d6d43fb553d5daa790f1b3945cda7be3b4430beb38745492a12c7f30b7866163955c5aff34225debb98a0524023ab54e90cc9b971536fd',
            role='Guardian',
            full_name='Grace Guardian',
            education='BA in Social Work',
            experience='5 years of experience in child care',
            bio='Guardian of a child with special needs.',
            phone='0400 000 001',
            register_time=datetime.now(timezone.utc)
        )
        db.session.add(guardian)
        db.session.commit()

        cls.server_thread = Thread(target=cls.app.run, kwargs={"use_reloader": False})
        cls.server_thread.daemon = True
        cls.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = "http://localhost:5000"

    @classmethod
    def tearDownClass(cls):
        print("[Teardown] Closing browser and cleaning up test environment")
        cls.driver.quit()
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_guardian_login_redirect(self):
        print("\n[Test 2] Attempting login and checking for Guardian dashboard redirect...")
        self.driver.get(f"{self.base_url}/login")

        email_input = self.driver.find_element(By.ID, "email")
        password_input = self.driver.find_element(By.ID, "password")
        email_input.send_keys("guardian@outlook.com")
        password_input.send_keys("112233")
        password_input.send_keys(Keys.RETURN)

        self.driver.implicitly_wait(3)
        self.assertIn("/guardian", self.driver.current_url)

        sidebar_heading = self.driver.find_element(By.XPATH, "//aside//h2")
        self.assertEqual(sidebar_heading.text.strip(), "Guardian")
        print("[✓] Test 2 passed: Guardian successfully logged in and redirected to dashboard.")
