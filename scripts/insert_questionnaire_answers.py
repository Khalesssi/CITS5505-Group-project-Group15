from app import create_app
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer
from app.models.patient import Patient
from app.models.user import User
from datetime import date

app = create_app()

with app.app_context():
    sw = User.query.filter_by(role='Support Worker').first()
    patients = Patient.query.all()

    if not sw or len(patients) == 0:
        print("Error: No support worker or patients found.")
    else:
        all_answers = []

        report_dates = [date(2024, 5, 1), date(2024, 5, 8), date(2024, 5, 14)]

        for i, patient in enumerate(patients):
            for j, report_date in enumerate(report_dates):
                answers = QuestionnaireAnswer(
                    support_worker_id=sw.id,
                    patient_id=patient.id,
                    report_date=report_date,
                    q1_emotion_stable='Yes' if (i + j) % 2 == 0 else 'No',
                    q2_pain_present='Yes' if (i + j + 1) % 2 == 0 else 'No',
                    q3_energy_level=1 + ((i + j) % 5),  # 1–5
                    q4_food_intake=['Normal', 'Reduced', 'Excessive'][(i + j) % 3],
                    q5_daily_activities='Yes' if (i + j) % 2 == 0 else 'No',
                    q6_physical_training=10 * ((i + j) % 11),  # 0–100
                    q7_post_exercise_pain=1 + ((i + j) % 10),  # 1–10
                    q8_balance_score=1 + ((i + j) % 5),        # 1–5
                    q9_self_care=1 + ((i + 2 * j) % 5),        # 1–5
                    q10_household_tasks=["Completed", "Partially Completed", "Not Completed"][(i + j) % 3],
                    q11_skill_learning=["Good", "Average", "Poor"][(i + 2 * j) % 3],
                    q12_emotional_fluctuations=1 + ((i + j) % 10),  # 1–10
                    q13_social_willingness=1 + ((j + i) % 5),       # 1–5
                    q14_therapist_response=1 + ((j + 2 * i) % 5),   # 1–5
                    q15_anxiety_depression='Yes' if (i + j) % 2 == 0 else 'No'
                )
                all_answers.append(answers)

        db.session.add_all(all_answers)
        db.session.commit()
        print(f"✅ Inserted {len(all_answers)} questionnaire answers for {len(patients)} patients.")
