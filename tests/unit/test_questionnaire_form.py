import unittest
from datetime import date
from app import create_app
from config import TestingConfig
from app.forms.questionnaire_forms import DailyReportForm

class QuestionnaireFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_daily_report_form_invalid_score(self):
        print("=== Test 9: DailyReportForm invalid question3 score started ===")

        with self.app.test_request_context():
            form = DailyReportForm(data={
                "patient_id": 1,
                "date": date.today(),

                # Valid fields
                "question1": "Yes",
                "question2": "No",
                "question3": 7,  # Invalid, range 1–5
                "question4": "Normal",
                "question5": "Yes",
                "question6": 50,
                "question7": 5,
                "question8": 4,
                "question9": 5,
                "question10": "Completed",
                "question11": "Good",
                "question12": 3,
                "question13": 4,
                "question14": 5,
                "question15": "No"
            })

            # Set SelectField choices (otherwise it will raise an error)
            form.patient_id.choices = [(1, "Test Patient")]
            form.question1.choices = [("Yes", "Yes"), ("No", "No")]
            form.question2.choices = [("Yes", "Yes"), ("No", "No")]
            form.question4.choices = [("Normal", "Normal"), ("Reduced", "Reduced"), ("Excessive", "Excessive")]
            form.question5.choices = [("Yes", "Yes"), ("No", "No")]
            form.question10.choices = [("Completed", "Completed"), ("Partially Completed", "Partially Completed"), ("Not Completed", "Not Completed")]
            form.question11.choices = [("Good", "Good"), ("Average", "Average"), ("Poor", "Poor")]
            form.question15.choices = [("Yes", "Yes"), ("No", "No")]

            self.assertFalse(form.validate(), "Form should fail because question3 exceeds allowed range")

        print("✅ Test 9 passed: Invalid question3 score correctly failed validation.\n")
