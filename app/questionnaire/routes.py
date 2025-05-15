from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer
from datetime import date
from app.models.patient import Patient
from app.questionnaire import questionnaire_bp
from flask import render_template
from datetime import datetime
from flask import jsonify
from app.models.user import User



# Route to submit questionnaire answers
@questionnaire_bp.route('/questionnaire', methods=['POST'])
@login_required
def submit_questionnaire():

    # Get the selected patient ID from the form
    patient_id = request.form.get('patient_id')
    if not patient_id:
        flash('Patient selection is required.')
        return redirect(url_for('dashboard.sw_dashboard'))
    
    # Get and validate the selected report date
    date_str = request.form.get('date')
    if not date_str:
        flash('Please select a date.')
        return redirect(url_for('dashboard.sw_dashboard'))

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format.')
        return redirect(url_for('dashboard.sw_dashboard'))

    # Collect answers for all 15 questions
    answers = {}
    for i in range(1, 16):
        q = f'question{i}'
        answers[q] = request.form.get(q)

    # Check if any question was left unanswered
    missing = [k for k, v in answers.items() if v is None]
    if missing:
        flash('Please answer all questions before submitting.')
        return redirect(url_for('dashboard.sw_dashboard'))

    # Create a new questionnaire entry
    new_entry = QuestionnaireAnswer(
        support_worker_id=current_user.id,
        patient_id=patient_id,
        report_date=selected_date,
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

    # Save the entry to the database
    db.session.add(new_entry)
    db.session.commit()
    flash('Report submitted successfully!')
    return redirect(url_for('dashboard.sw_dashboard'))

# AJAX endpoint: get all patients
@questionnaire_bp.route('/ajax_get_patients')
@login_required
def ajax_get_patients():
    patients = Patient.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in patients])

# AJAX endpoint: get all report dates for a specific patient
@questionnaire_bp.route('/ajax_get_dates_by_patient/<int:patient_id>')
@login_required
def ajax_get_dates_by_patient(patient_id):
    dates = (
        db.session.query(QuestionnaireAnswer.report_date)
        .filter_by(patient_id=patient_id)
        .distinct()
        .order_by(QuestionnaireAnswer.report_date.desc())
        .all()
    )
    return jsonify([d.report_date.strftime('%Y-%m-%d') for d in dates])

# AJAX endpoint: get a specific report for a patient by date
@questionnaire_bp.route('/ajax_get_report/<int:patient_id>/<string:report_date>')
@login_required
def ajax_get_report(patient_id, report_date):
    from datetime import datetime
    try:
        parsed_date = datetime.strptime(report_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Query the report
    report = QuestionnaireAnswer.query.filter_by(patient_id=patient_id, report_date=parsed_date).first()
    if not report:
        return jsonify({'error': 'No report found'}), 404

    # Get support worker information
    sw = User.query.get(report.support_worker_id)

    # Return report content in JSON format
    return jsonify({
        'support_worker_name': sw.full_name if sw else 'Unknown',
        'answers': {
            'q1': report.q1_emotion_stable,
            'q2': report.q2_pain_present,
            'q3': report.q3_energy_level,
            'q4': report.q4_food_intake,
            'q5': report.q5_daily_activities,
            'q6': report.q6_physical_training,
            'q7': report.q7_post_exercise_pain,
            'q8': report.q8_balance_score,
            'q9': report.q9_self_care,
            'q10': report.q10_household_tasks,
            'q11': report.q11_skill_learning,
            'q12': report.q12_emotional_fluctuations,
            'q13': report.q13_social_willingness,
            'q14': report.q14_therapist_response,
            'q15': report.q15_anxiety_depression
        }
    })
