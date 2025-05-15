import unittest
from threading import Thread
from selenium import webdriver
from app import create_app
from config import TestingConfig
from app.extensions import db

class AccessControlTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[Setup] Starting Flask test server for access control test...")

        cls.app = create_app(TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.server_thread = Thread(target=cls.app.run, kwargs={"use_reloader": False})
        cls.server_thread.daemon = True
        cls.server_thread.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = "http://localhost:5000"

    @classmethod
    def tearDownClass(cls):
        print("[Teardown] Closing browser and cleaning up environment")
        cls.driver.quit()
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_unauthenticated_access_redirect(self):
        print("\n[Test 3] Verifying unauthenticated access to /dashboard/guardian is redirected to /login")
        self.driver.get(f"{self.base_url}/dashboard/guardian")

        # Flask-Login should redirect to /login if unauthenticated
        self.assertIn("/login", self.driver.current_url)
        print("[✓] Test 3 passed: Unauthenticated access was redirected to /login")
