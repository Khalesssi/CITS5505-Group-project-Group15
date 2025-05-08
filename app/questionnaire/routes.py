from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer
from datetime import date

bp = Blueprint('questionnaire', __name__)

@bp.route('/submit_questionnaire', methods=['POST'])
@login_required
def submit_questionnaire():
    # print(request.form)

    patient_id = request.form.get('patient_id')
    if not patient_id:
        flash('Patient selection is required.')
        return redirect(url_for('dashboard.sw_dashboard'))

    answers = {}
    for i in range(1, 16):
        q = f'question{i}'
        answers[q] = request.form.get(q)

    missing = [k for k, v in answers.items() if v is None]
    if missing:
        flash('Please answer all questions before submitting.')
        return redirect(url_for('dashboard.sw_dashboard'))

    new_entry = QuestionnaireAnswer(
        support_worker_id=current_user.id,
        patient_id=patient_id,
        # report_date=date.today(),
        q1_emotion_stable=answers['question1'],
        q2_pain_present=answers['question2'],
        q3_energy_level=answers['question3'],
        q4_food_intake=answers['question4'],
        q5_daily_activities=answers['question5'],
        q6_physical_training=answers['question6'],
        q7_post_exercise_pain=answers['question7'],
        q8_balance_score=answers['question8'],
        q9_self_care=answers['question9'],
        q10_household_tasks=answers['question10'],
        q11_skill_learning=answers['question11'],
        q12_emotional_fluctuations=answers['question12'],
        q13_social_willingness=answers['question13'],
        q14_therapist_response=answers['question14'],
        q15_anxiety_depression=answers['question15']
    )

    db.session.add(new_entry)
    db.session.commit()
    flash('Report submitted successfully!')
    return redirect(url_for('dashboard.sw_dashboard'))