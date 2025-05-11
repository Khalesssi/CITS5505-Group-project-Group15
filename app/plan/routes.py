from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.extensions import db
from app.plan import plan_bp
from app.utils.role_mapping import specialty_to_field
from app.utils.role_mapping import role_to_patient_field
from datetime import datetime
from collections import defaultdict
from app.models.user import User
from flask import jsonify
from app.utils.role_mapping import role_to_patient_field
from app.utils.role_mapping import specialty_to_field

@plan_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_plan():
    field_name = specialty_to_field.get(current_user.specialty)
    if not field_name:
        flash("Invalid therapist specialty.")
        return redirect(url_for("dashboard.dashboard_redirect"))

    patients = Patient.query.filter(getattr(Patient, field_name) == current_user.id).all()

    if request.method == 'POST':
        patient_id = request.form.get("patient_id")
        content = request.form.get("content")
        plan_date_str = request.form.get("plan_date")
        share_guardian = request.form.get("share_guardian") == "on"
        share_sw = request.form.get("share_sw") == "on"

        try:
            plan_date = datetime.strptime(plan_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date format.")
            return redirect(url_for('dashboard.therapist_dashboard'))

        plan = SupportPlan(
            patient_id=patient_id,
            therapist_id=current_user.id,
            content=content,
            date=plan_date,
            share_with_guardian=share_guardian,
            share_with_sw=share_sw
        )
        db.session.add(plan)
        db.session.commit()
        flash("Support plan submitted and shared.")
        return redirect(url_for('dashboard.therapist_dashboard'))

    return render_template('plan/submit_plan.html', patients=patients)

@plan_bp.route('/ajax_get_shared_support_plans')
@login_required
def ajax_get_shared_support_plans():
    role = current_user.role
    if role == "Guardian":
        share_field = SupportPlan.share_with_guardian
        patient_field = Patient.guardian_id
    elif role == "Support Worker":
        share_field = SupportPlan.share_with_sw
        patient_field = Patient.sw_id
    else:
        return jsonify({"error": "Unauthorized"}), 403

    patient_id = request.args.get('patient_id', type=int)
    date_str = request.args.get('plan_date')
    if not patient_id or not date_str:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # 安全校验：只能访问自己绑定的病人
    patient = Patient.query.get(patient_id)
    if not patient or getattr(patient, patient_field.name) != current_user.id:
        return jsonify({'error': 'Unauthorized access to patient data'}), 403

    plans = SupportPlan.query.filter(
        SupportPlan.patient_id == patient_id,
        share_field == True
    ).all()

    filtered = [p for p in plans if p.date.date() == selected_date]

    grouped = defaultdict(list)
    for plan in filtered:
        therapist = User.query.get(plan.therapist_id)
        if therapist and therapist.specialty:
            grouped[therapist.specialty].append(plan.content)

    return jsonify(grouped)