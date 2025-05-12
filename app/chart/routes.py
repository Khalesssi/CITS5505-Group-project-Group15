# app/chart/routes.py
from flask import render_template, request, jsonify, Response
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.questionnaire import QuestionnaireAnswer
import csv
import io
from . import chart_bp



# Entry point


# API：Get all patient name in database
@chart_bp.route('/patients')
@login_required
def get_patient_names():
    patients = Patient.query.all()
    names = [p.name for p in patients]
    return jsonify(names)

# API: Get chart data, filtered by specialty and optionally by patient
@chart_bp.route('/chart-data')
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
    general_data = query.with_entities(
        QuestionnaireAnswer.q1_emotion_stable,
        QuestionnaireAnswer.q2_pain_present,
        QuestionnaireAnswer.q3_energy_level,
        QuestionnaireAnswer.q4_food_intake,
        QuestionnaireAnswer.q5_daily_activities
    ).all()

    emotion = {"Yes": 0, "No": 0}
    pain = {"Yes": 0, "No": 0}
    food = {"Normal": 0, "Reduced": 0, "Excessive": 0}
    activity = {"Yes": 0, "No": 0}
    energy_total = 0
    energy_count = 0

    for r in general_data:
        q1, q2, q3, q4, q5 = r
        if q1 in emotion: emotion[q1] += 1
        if q2 in pain: pain[q2] += 1
        if q3 is not None:
            energy_total += q3
            energy_count += 1
        if q4 in food: food[q4] += 1
        if q5 in activity: activity[q5] += 1

    energy_avg = round(energy_total / energy_count, 2) if energy_count else 0
#-------------------------Physio char------------------------------------------
    if specialty == 'physio':
        data = query.with_entities(
            QuestionnaireAnswer.q6_physical_training,
            QuestionnaireAnswer.q7_post_exercise_pain,
            QuestionnaireAnswer.q8_balance_score,
            QuestionnaireAnswer.report_date
        ).all()
        # Result return format：[["q6", "q7", "q8"], ...]
        return jsonify({
            "specialty": specialty,
            "data": [list(r) for r in data],
            "general": {
                "emotion_stable": emotion,
                "pain_present": pain,
                "energy_avg": energy_avg,
                "food_intake": food,
                "daily_activities": activity
            }
        })

#-------------------------OT char------------------------------------------
    elif specialty == 'ot':
        data = query.with_entities(
            QuestionnaireAnswer.q9_self_care,
            QuestionnaireAnswer.q10_household_tasks,
            QuestionnaireAnswer.q11_skill_learning,
            QuestionnaireAnswer.report_date
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
                r[3]          # report_date
            ])

        return jsonify({
            "specialty": specialty,
            "data": formatted,
            "general": {
                "emotion_stable": emotion,
                "pain_present": pain,
                "energy_avg": energy_avg,
                "food_intake": food,
                "daily_activities": activity
            }
        })

#-------------------------psych char------------------------------------------
    elif specialty == 'psych':
        data = query.with_entities(
            QuestionnaireAnswer.q12_emotional_fluctuations,
            QuestionnaireAnswer.q13_social_willingness,
            QuestionnaireAnswer.q14_therapist_response,
            QuestionnaireAnswer.q15_anxiety_depression,
            QuestionnaireAnswer.report_date
        ).all()

    # mapping q15：Yes -> 1, No -> 0
        depression_map = {'Yes': 1, 'No': 0}
    
        formatted = []
        for r in data:
            mapped_depression = depression_map.get(r[3], 0)
            formatted.append([
                r[0],  # q12_emotional_fluctuations
                r[1],  # q13_social_willingness
                r[2],  # q14_therapist_response
                mapped_depression,  # q15_anxiety_depression
                r[4]   # report_date
            ])

        return jsonify({
            "specialty": specialty,
            "data": formatted,
            "general": {
                "emotion_stable": emotion,
                "pain_present": pain,
                "energy_avg": energy_avg,
                "food_intake": food,
                "daily_activities": activity
            }
        })



@chart_bp.route('/download_data')
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
            QuestionnaireAnswer.report_date
        ).all()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Patient', 'Physical Training', 'Post-exercise Pain', 'Balance Score', 'Submitted At'])
        for row in data:
            name, q6, q7, q8, report_date = row
            writer.writerow([name, q6, q7, q8, report_date.strftime('%Y-%m-%d')])

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
            QuestionnaireAnswer.report_date
        ).all()

        # Map string to numeric value
        task_map = {'Completed': 5, 'Partially': 3, 'Not': 0}
        skill_map = {'Good': 5, 'Average': 3, 'Poor': 1}

        # CSV
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
            QuestionnaireAnswer.report_date
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

