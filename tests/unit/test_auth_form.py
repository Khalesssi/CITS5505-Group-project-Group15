import unittest
from app import create_app
from config import TestingConfig
from app.forms.auth_forms import RegisterForm

class RegisterFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_register_form_invalid_email(self):
        print("=== Test 7: RegisterForm invalid email started ===")

        with self.app.app_context():
            form = RegisterForm(data={
                "email": "notanemail",  # ❌ Invalid email
                "password": "123456",
                "role": "Guardian"
            })
            self.assertFalse(form.validate(), "Form should be invalid due to bad email")

        print(" Test 7 passed: Invalid email correctly failed validation.\n")
