from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.extensions import db
from app.plan import plan_bp
from app.utils.role_mapping import specialty_to_field, role_to_patient_field
from datetime import datetime
from collections import defaultdict
from app.models.user import User

from app.forms.plan_forms import SupportPlanForm

@plan_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_plan():
    field_name = specialty_to_field.get(current_user.specialty)
    if not field_name:
        flash("Invalid therapist specialty.")
        return redirect(url_for("dashboard.dashboard_redirect"))

    patients = Patient.query.filter(getattr(Patient, field_name) == current_user.id).all()
    form = SupportPlanForm()

    # Dynamic population select
    form.patient_id.choices = [(p.id, p.name) for p in patients]

    if form.validate_on_submit():
        plan = SupportPlan(
            patient_id=form.patient_id.data,
            therapist_id=current_user.id,
            content=form.content.data,
            date=form.plan_date.data,
            share_with_guardian=form.share_guardian.data,
            share_with_sw=form.share_sw.data
        )
        db.session.add(plan)
        db.session.commit()
        flash("Support plan submitted and shared.")
        return redirect(url_for('dashboard.therapist_dashboard'))

    return render_template('plan/submit_plan.html', form=form)


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

    # Security check: Only allow access to patients bound to the current user
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

# Addition: Retrieve all available dates of shared support plans for a specific patient
@plan_bp.route('/ajax_get_plan_dates_by_patient/<int:patient_id>')
@login_required
def ajax_get_plan_dates_by_patient(patient_id):
    role = current_user.role
    if role == "Guardian":
        share_field = SupportPlan.share_with_guardian
        patient_field = Patient.guardian_id
    elif role == "Support Worker":
        share_field = SupportPlan.share_with_sw
        patient_field = Patient.sw_id
    else:
        return jsonify({"error": "Unauthorized"}), 403

    patient = Patient.query.get(patient_id)
    if not patient or getattr(patient, patient_field.name) != current_user.id:
        return jsonify({'error': 'Unauthorized access to patient data'}), 403

    plans = (
        SupportPlan.query
        .filter(SupportPlan.patient_id == patient_id, share_field == True)
        .with_entities(SupportPlan.date)
        .order_by(SupportPlan.date.desc())
        .all()
    )

    unique_dates = sorted(list({p.date.date().isoformat() for p in plans}))
    return jsonify(unique_dates)
