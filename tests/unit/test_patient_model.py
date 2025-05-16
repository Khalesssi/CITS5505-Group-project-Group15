import unittest
from datetime import date, datetime, timezone
from werkzeug.security import generate_password_hash
from app import create_app
from config import TestingConfig
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient

class PatientModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_patient_creation_with_roles(self):
        print("=== Test 3: Patient creation with full role bindings started ===")

        # Create 6 related users
        guardian = User(email="g@example.com", password_hash=generate_password_hash("123"), role="Guardian")
        sw = User(email="sw@example.com", password_hash=generate_password_hash("123"), role="Support Worker")
        physio = User(email="p1@example.com", password_hash=generate_password_hash("123"), role="Therapist", specialty="physio")
        ot = User(email="p2@example.com", password_hash=generate_password_hash("123"), role="Therapist", specialty="ot")
        psych = User(email="p3@example.com", password_hash=generate_password_hash("123"), role="Therapist", specialty="psych")

        db.session.add_all([guardian, sw, physio, ot, psych])
        db.session.commit()

        patient = Patient(
            name="Test Patient",
            date_of_birth=date(2010, 1, 1),
            gender="Female",
            guardian_id=guardian.id,
            sw_id=sw.id,
            physio_id=physio.id,
            ot_id=ot.id,
            psych_id=psych.id,
            medical_info="Test medical info",
            notes="Some notes"
        )
        db.session.add(patient)
        db.session.commit()

        queried = Patient.query.filter_by(name="Test Patient").first()
        self.assertIsNotNone(queried, "Patient should be created and found in database")
        self.assertEqual(queried.guardian_id, guardian.id)
        self.assertEqual(queried.sw_id, sw.id)
        self.assertEqual(queried.physio_id, physio.id)
        self.assertEqual(queried.ot_id, ot.id)
        self.assertEqual(queried.psych_id, psych.id)

        print("=== Test 3 passed: Patient created and linked to correct users ===\n")
