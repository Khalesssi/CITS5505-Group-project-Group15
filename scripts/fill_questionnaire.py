from app import create_app
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer
from datetime import date

app = create_app()

with app.app_context():
    # 创建两条问卷回答记录（每个病人一条）
    answer1 = QuestionnaireAnswer(
        support_worker_id=2,
        patient_id=1,
        report_date=date(2025, 5, 10),

        q1_emotion_stable='1',
        q2_pain_present='0',
        q3_energy_level=4,
        q4_food_intake='Normal',
        q5_daily_activities='1',
        q6_physical_training=75,
        q7_post_exercise_pain=3,
        q8_balance_score=4,
        q9_self_care=4,
        q10_household_tasks='Completed',
        q11_skill_learning='Good',
        q12_emotional_fluctuations=2,
        q13_social_willingness=4,
        q14_therapist_response=5,
        q15_anxiety_depression='0'
    )

    answer2 = QuestionnaireAnswer(
        support_worker_id=2,
        patient_id=2,
        report_date=date(2025, 5, 11),

        q1_emotion_stable='0',
        q2_pain_present='1',
        q3_energy_level=2,
        q4_food_intake='Reduced',
        q5_daily_activities='0',
        q6_physical_training=30,
        q7_post_exercise_pain=6,
        q8_balance_score=2,
        q9_self_care=3,
        q10_household_tasks='Partially',
        q11_skill_learning='Average',
        q12_emotional_fluctuations=5,
        q13_social_willingness=2,
        q14_therapist_response=3,
        q15_anxiety_depression='1'
    )

    db.session.add_all([answer1, answer2])
    db.session.commit()
    print("✅ Questionnaire answers inserted successfully!")
