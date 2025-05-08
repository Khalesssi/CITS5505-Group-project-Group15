# app/chart/routes.py
from flask import Blueprint, render_template, request, jsonify, Response
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.questionnaire import QuestionnaireAnswer
import csv
import io

bp = Blueprint('chart', __name__, url_prefix='/chart')

# Entry point
@bp.route('/therapist/chart')
@login_required
def therapist_chart():
    if current_user.role != 'Therapist':
        return "Access Denied", 403

    specialty = current_user.specialty.lower()
    return render_template("chart/therapist_chart.html", specialty=specialty)

# API：Get all patient name in database
@bp.route('/therapist/patients')
@login_required
def get_patient_names():
    patients = Patient.query.all()
    names = [p.name for p in patients]
    return jsonify(names)

# API: Get chart data, filtered by specialty and optionally by patient
@bp.route('/therapist/chart-data')
@login_required
def get_chart_data():
    if current_user.role != 'Therapist':
        return jsonify({'error': 'Access denied'}), 403

    patient_name = request.args.get('patient')
    specialty = current_user.specialty.lower()

    query = QuestionnaireAnswer.query.join(Patient)

    if patient_name and patient_name != 'All':
        query = query.filter(Patient.name == patient_name)

    # Return different fields of data based on therapist type
#-------------------------Physio char------------------------------------------
    if specialty == 'physio':
        data = query.with_entities(
            QuestionnaireAnswer.q6_physical_training,
            QuestionnaireAnswer.q7_post_exercise_pain,
            QuestionnaireAnswer.q8_balance_score,
            QuestionnaireAnswer.submitted_at
        ).all()
        # Result return format：[["q6", "q7", "q8"], ...]
        return jsonify({
        "specialty": specialty,
        "data": [list(r) for r in data]
    })
#-------------------------OT char------------------------------------------
    elif specialty == 'ot':
        data = query.with_entities(
            QuestionnaireAnswer.q9_self_care,
            QuestionnaireAnswer.q10_household_tasks,
            QuestionnaireAnswer.q11_skill_learning,
            QuestionnaireAnswer.submitted_at
        ).all()

        # dictionary for mapping
        task_map = {'Completed': 5, 'Partially': 3, 'Not': 0}
        skill_map = {'Good': 5, 'Average': 3, 'Poor': 1}

        formatted = []
        for r in data:
            task_score = task_map.get(r[1], 0)
            skill_score = skill_map.get(r[2], 0)
            formatted.append([
                r[0],         # q9_self_care
                task_score,   # mapped q10_household_tasks
                skill_score,  # mapped q11_skill_learning
                r[3]          # submitted_at
            ])

        return jsonify({
        "specialty": specialty,
        "data": formatted
        })
#-------------------------psych char------------------------------------------
    elif specialty == 'psych':
        data = query.with_entities(
            QuestionnaireAnswer.q12_emotional_fluctuations,
            QuestionnaireAnswer.q13_social_willingness,
            QuestionnaireAnswer.q14_therapist_response,
            QuestionnaireAnswer.q15_anxiety_depression,
            QuestionnaireAnswer.submitted_at
        ).all()

    # 映射 q15：Yes -> 1, No -> 0
        depression_map = {'Yes': 1, 'No': 0}
    
        formatted = []
        for r in data:
            mapped_depression = depression_map.get(r[3], 0)
            formatted.append([
                r[0],  # q12_emotional_fluctuations
                r[1],  # q13_social_willingness
                r[2],  # q14_therapist_response
                mapped_depression,  # q15_anxiety_depression
                r[4]   # submitted_at
            ])

        return jsonify({
        "specialty": specialty,
        "data": formatted
        })

    else:
        
        data = query.with_entities(
            QuestionnaireAnswer.q1_emotion_stable,
            QuestionnaireAnswer.q2_pain_present,
            QuestionnaireAnswer.q3_energy_level,
            QuestionnaireAnswer.q4_food_intake,
            QuestionnaireAnswer.q5_daily_activities
        ).all()
        return jsonify([list(r) for r in data])





@bp.route('/therapist/download-data')
@login_required
def download_data():
    if current_user.role != 'Therapist':
        return "Forbidden", 403

    specialty = current_user.specialty.lower()
    query = QuestionnaireAnswer.query.join(Patient)

#-------------------------Physio csv------------------------------------------
    if specialty == 'physio':
        data = query.with_entities(
            Patient.name,
            QuestionnaireAnswer.q6_physical_training,
            QuestionnaireAnswer.q7_post_exercise_pain,
            QuestionnaireAnswer.q8_balance_score,
            QuestionnaireAnswer.submitted_at
        ).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Patient', 'Physical Training', 'Post-exercise Pain', 'Balance Score', 'Submitted At'])
        for row in data:
            name, q6, q7, q8, submitted_at = row
            writer.writerow([name, q6, q7, q8, submitted_at.strftime('%Y-%m-%d')])

        output.seek(0)
        return Response(output.getvalue(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=physio_data.csv"})
    
#-------------------------ot csv------------------------------------------
    if specialty == 'ot':
        data = query.with_entities(
            Patient.name,
            QuestionnaireAnswer.q9_self_care,
            QuestionnaireAnswer.q10_household_tasks,
            QuestionnaireAnswer.q11_skill_learning,
            QuestionnaireAnswer.submitted_at
        ).all()

        # Map string to numeric value
        task_map = {'Completed': 5, 'Partially': 3, 'Not': 0}
        skill_map = {'Good': 5, 'Average': 3, 'Poor': 1}

        # 生成 CSV
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Patient', 'Self Care Score', 'Task Score', 'Skill Score', 'Submitted At'])
        for row in data:
            name, q9, q10, q11, date = row
            task_score = task_map.get(q10, 0)
            skill_score = skill_map.get(q11, 0)
            writer.writerow([name, q9, task_score, skill_score, date.strftime('%Y-%m-%d')])

        output.seek(0)
        return Response(output.getvalue(), mimetype='text/csv',
                        headers={"Content-Disposition": "attachment; filename=ot_data.csv"})
    
#-------------------------psyth csv------------------------------------------

    elif specialty == 'psych':
        data = query.with_entities(
            Patient.name,
            QuestionnaireAnswer.q12_emotional_fluctuations,
            QuestionnaireAnswer.q13_social_willingness,
            QuestionnaireAnswer.q14_therapist_response,
            QuestionnaireAnswer.q15_anxiety_depression,
            QuestionnaireAnswer.submitted_at
        ).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Patient', 'Emotional Fluctuations', 'Social Willingness', 'Therapist Response', 'Anxiety/Depression', 'Submitted At'])

        for row in data:
            name, q12, q13, q14, q15, date = row
            writer.writerow([name, q12, q13, q14, q15, date.strftime('%Y-%m-%d')])

        output.seek(0)
        return Response(output.getvalue(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=psych_data.csv"})

    return "Unsupported therapist type", 400