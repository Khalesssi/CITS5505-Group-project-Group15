import unittest
from datetime import date, datetime
from werkzeug.security import generate_password_hash
from app import create_app
from config import TestingConfig
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.support_plan import SupportPlan

class RouteAuthorizationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Insert dummy therapist (id=1) to avoid foreign key conflict
        therapist = User(
            id=1,
            email="therapist@example.com",
            password_hash=generate_password_hash("pass123"),
            role="Therapist",
            specialty="psych"
        )
        db.session.add(therapist)

        # Create two Guardian users
        self.guardian = User(
            email="g1@example.com",
            password_hash=generate_password_hash("123456"),
            role="Guardian"
        )
        self.other_guardian = User(
            email="g2@example.com",
            password_hash=generate_password_hash("123456"),
            role="Guardian"
        )
        db.session.add_all([self.guardian, self.other_guardian])
        db.session.commit()

        # Create two patients
        self.bound_patient = Patient(
            name="Bound Patient",
            date_of_birth=date(2010, 5, 15),
            gender="Female",
            guardian_id=self.guardian.id
        )
        self.other_patient = Patient(
            name="Other Patient",
            date_of_birth=date(2011, 6, 20),
            gender="Male",
            guardian_id=self.other_guardian.id
        )
        db.session.add_all([self.bound_patient, self.other_patient])
        db.session.commit()

        # Add a shared support plan for bound_patient
        sp = SupportPlan(
            patient_id=self.bound_patient.id,
            therapist_id=therapist.id,
            content="Weekly plan.",
            date=datetime(2025, 5, 15, 10, 0),
            share_with_guardian=True
        )
        db.session.add(sp)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_as_guardian(self):
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.guardian.id)
            sess["_fresh"] = True

    def test_guardian_access_bound_patient(self):
        print("=== Test 10-A: Guardian access to their own patient ===")

        self.login_as_guardian()
        url = f"/plan/ajax_get_plan_dates_by_patient/{self.bound_patient.id}"  # Path correction
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("2025-05-15", response.get_data(as_text=True))

        print("✅ Passed: Guardian received shared dates for bound patient.\n")

    def test_guardian_access_other_patient(self):
        print("=== Test 10-B: Guardian access to unbound patient (should fail) ===")

        self.login_as_guardian()
        url = f"/plan/ajax_get_plan_dates_by_patient/{self.other_patient.id}"  # Path correction
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertIn("Unauthorized", response.get_data(as_text=True))

        print(" Passed: Guardian denied access to unbound patient.\n")
