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
from app.forms.questionnaire_forms import DailyReportForm

@questionnaire_bp.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def submit_questionnaire():
    form = DailyReportForm()

    # 绑定病人 choices
    patients = Patient.query.filter_by(sw_id=current_user.id).all()
    form.patient_id.choices = [(p.id, p.name) for p in patients]

    if form.validate_on_submit():
        new_entry = QuestionnaireAnswer(
            support_worker_id=current_user.id,
            patient_id=form.patient_id.data,
            report_date=form.date.data,
            q1_emotion_stable=form.question1.data,
            q2_pain_present=form.question2.data,
            q3_energy_level=form.question3.data,
            q4_food_intake=form.question4.data,
            q5_daily_activities=form.question5.data,
            q6_physical_training=form.question6.data,
            q7_post_exercise_pain=form.question7.data,
            q8_balance_score=form.question8.data,
            q9_self_care=form.question9.data,
            q10_household_tasks=form.question10.data,
            q11_skill_learning=form.question11.data,
            q12_emotional_fluctuations=form.question12.data,
            q13_social_willingness=form.question13.data,
            q14_therapist_response=form.question14.data,
            q15_anxiety_depression=form.question15.data
        )
        db.session.add(new_entry)
        db.session.commit()
        flash("Report submitted successfully!")
        return redirect(url_for('dashboard.sw_dashboard'))

    return render_template('dashboard/sw.html', form=form, patients=patients)


@questionnaire_bp.route('/ajax_get_patients')
@login_required
def ajax_get_patients():
    patients = Patient.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in patients])

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

@questionnaire_bp.route('/ajax_get_report/<int:patient_id>/<string:report_date>')
@login_required
def ajax_get_report(patient_id, report_date):
    from datetime import datetime
    try:
        parsed_date = datetime.strptime(report_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    report = QuestionnaireAnswer.query.filter_by(patient_id=patient_id, report_date=parsed_date).first()
    if not report:
        return jsonify({'error': 'No report found'}), 404

    sw = User.query.get(report.support_worker_id)

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
