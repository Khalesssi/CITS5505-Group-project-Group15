import unittest
from datetime import date, datetime, timezone
from werkzeug.security import generate_password_hash
from app import create_app
from config import TestingConfig
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.questionnaire import QuestionnaireAnswer

class QuestionnaireModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_questionnaire_valid_submission(self):
        print("=== Test 5: Valid questionnaire submission started ===")

        # 创建 Support Worker 和 Patient
        sw = User(email="sw@example.com", password_hash=generate_password_hash("123456"), role="Support Worker")
        guardian = User(email="g@example.com", password_hash=generate_password_hash("123456"), role="Guardian")

        db.session.add_all([sw, guardian])
        db.session.commit()

        patient = Patient(
            name="QPatient",
            date_of_birth=date(2011, 5, 1),
            gender="Female",
            guardian_id=guardian.id
        )
        db.session.add(patient)
        db.session.commit()

        # 创建合法问卷数据
        answer = QuestionnaireAnswer(
            support_worker_id=sw.id,
            patient_id=patient.id,
            report_date=date.today(),

            q1_emotion_stable='Yes',
            q2_pain_present='No',
            q3_energy_level=4,
            q4_food_intake='Normal',
            q5_daily_activities='Yes',
            q6_physical_training=60,
            q7_post_exercise_pain=2,
            q8_balance_score=4,
            q9_self_care=5,
            q10_household_tasks='Completed',

            q11_skill_learning='Good',
            q12_emotional_fluctuations=1,
            q13_social_willingness=4,
            q14_therapist_response=5,
            q15_anxiety_depression='No'
        )

        db.session.add(answer)
        db.session.commit()

        # 验证插入
        queried = QuestionnaireAnswer.query.filter_by(patient_id=patient.id).first()
        self.assertIsNotNone(queried, "Questionnaire answer should exist")
        self.assertEqual(queried.q3_energy_level, 4)
        self.assertEqual(queried.q15_anxiety_depression, 'No')

        print("=== Test 5 passed: Questionnaire answer inserted and verified ===\n")
