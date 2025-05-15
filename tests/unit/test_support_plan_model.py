import unittest
from datetime import datetime, date
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from app import create_app
from config import TestingConfig
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.support_plan import SupportPlan

class SupportPlanTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    #  Test 4: Normal support plan insertion
    def test_support_plan_creation(self):
        print("=== Test 4: Support plan creation started ===")

        therapist = User(
            email="therapist@example.com",
            password_hash=generate_password_hash("pass123"),
            role="Therapist",
            specialty="psych"
        )
        guardian = User(
            email="g@example.com",
            password_hash=generate_password_hash("pass123"),
            role="Guardian"
        )
        patient = Patient(
            name="PlanPatient",
            date_of_birth=datetime(2010, 1, 1).date(),
            gender="Male",
            guardian_id=1  # placeholder, will be replaced
        )

        db.session.add_all([therapist, guardian])
        db.session.commit()

        patient.guardian_id = guardian.id
        db.session.add(patient)
        db.session.commit()

        plan = SupportPlan(
            patient_id=patient.id,
            therapist_id=therapist.id,
            content="Weekly therapy and home training.",
            date=datetime(2025, 5, 15, 10, 0),
            share_with_guardian=True,
            share_with_sw=False
        )
        db.session.add(plan)
        db.session.commit()

        queried = SupportPlan.query.filter_by(patient_id=patient.id).first()
        self.assertIsNotNone(queried, "Support plan should be stored")
        self.assertEqual(queried.therapist_id, therapist.id)
        self.assertTrue(queried.share_with_guardian)
        self.assertFalse(queried.share_with_sw)

        print("=== Test 4 passed: Support plan created and fields verified ===\n")

    # Test 6: Support plan with missing content field should trigger an error
    def test_support_plan_missing_content(self):
        print("=== Test 6: Support plan missing content started ===")

        therapist = User(
            email="therapist2@example.com",
            password_hash=generate_password_hash("pass123"),
            role="Therapist",
            specialty="physio"
        )
        guardian = User(
            email="g2@example.com",
            password_hash=generate_password_hash("pass123"),
            role="Guardian"
        )
        db.session.add_all([therapist, guardian])
        db.session.commit()

        patient = Patient(
            name="MissingContentPatient",
            date_of_birth=date(2012, 2, 2),
            gender="Male",
            guardian_id=guardian.id
        )
        db.session.add(patient)
        db.session.commit()

        plan = SupportPlan(
            patient_id=patient.id,
            therapist_id=therapist.id,
            content=None,  #  Intentionally omit required fields
            date=datetime(2025, 5, 15, 10, 0),
            share_with_guardian=True,
            share_with_sw=True
        )

        db.session.add(plan)

        with self.assertRaises(IntegrityError, msg="Missing content should raise an IntegrityError"):
            db.session.commit()
        
        print("Test 6 passed: IntegrityError correctly raised for missing content.\n")
