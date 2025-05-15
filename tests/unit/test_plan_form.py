import unittest
from datetime import datetime
from app import create_app
from config import TestingConfig
from app.forms.plan_forms import SupportPlanForm

class SupportPlanFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_support_plan_form_valid(self):
        print("=== Test 8: SupportPlanForm valid data started ===")

        with self.app.test_request_context():
            form = SupportPlanForm(data={
                "patient_id": 1,
                "plan_date": "2025-05-15T10:00",
                "content": "Support plan for weekly training and rehab.",
                "share_guardian": True,
                "share_sw": False
            })

            # Key fix: Specify valid choices
            form.patient_id.choices = [(1, "Test Patient")]

            self.assertTrue(form.validate(), "Form should be valid with correct input and choices")

        print("✅ Test 8 passed: SupportPlanForm validated successfully.\n")
