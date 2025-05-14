from app import create_app
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer
from app.models.patient import Patient
from app.models.user import User
from datetime import date

app = create_app()

with app.app_context():
    # 获取已有 SW 和 Patient
    sw = User.query.filter_by(role='Support Worker').first()
    patients = Patient.query.all()

    if not sw or len(patients) == 0:
        print("Error: No support worker or patients found.")
    else:
        all_answers = []
        for patient in patients:
            answers = [
                QuestionnaireAnswer(
                    support_worker_id=sw.id,
                    patient_id=patient.id,
                    report_date=date(2024, 5, 1),
                    q1_emotion_stable='1',
                    q2_pain_present='0',
                    q3_energy_level=4,
                    q4_food_intake='Normal',
                    q5_daily_activities='1',
                    q6_physical_training=60,
                    q7_post_exercise_pain=3,
                    q8_balance_score=4,
                    q9_self_care=5,
                    q10_household_tasks='Completed',
                    q11_skill_learning='Good',
                    q12_emotional_fluctuations=1,
                    q13_social_willingness=4,
                    q14_therapist_response=5,
                    q15_anxiety_depression='0'
                ),
                QuestionnaireAnswer(
                    support_worker_id=sw.id,
                    patient_id=patient.id,
                    report_date=date(2024, 5, 8),
                    q1_emotion_stable='0',
                    q2_pain_present='1',
                    q3_energy_level=2,
                    q4_food_intake='Reduced',
                    q5_daily_activities='0',
                    q6_physical_training=30,
                    q7_post_exercise_pain=6,
                    q8_balance_score=3,
                    q9_self_care=3,
                    q10_household_tasks='Partially',
                    q11_skill_learning='Average',
                    q12_emotional_fluctuations=4,
                    q13_social_willingness=2,
                    q14_therapist_response=3,
                    q15_anxiety_depression='1'
                ),
                QuestionnaireAnswer(
                    support_worker_id=sw.id,
                    patient_id=patient.id,
                    report_date=date(2024, 5, 14),
                    q1_emotion_stable='1',
                    q2_pain_present='1',
                    q3_energy_level=3,
                    q4_food_intake='Excessive',
                    q5_daily_activities='1',
                    q6_physical_training=80,
                    q7_post_exercise_pain=2,
                    q8_balance_score=5,
                    q9_self_care=4,
                    q10_household_tasks='Completed',
                    q11_skill_learning='Good',
                    q12_emotional_fluctuations=2,
                    q13_social_willingness=5,
                    q14_therapist_response=4,
                    q15_anxiety_depression='0'
                )
            ]
            all_answers.extend(answers)

        db.session.add_all(all_answers)
        db.session.commit()
        print(f"Inserted {len(all_answers)} questionnaire answers for {len(patients)} patients.")
