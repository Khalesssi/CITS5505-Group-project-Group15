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

# Route for creating and submitting new support plans by therapists
@plan_bp.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_plan():
    # Map therapist specialty to corresponding patient field (psych_id, physio_id, ot_id)
    field_name = specialty_to_field.get(current_user.specialty)
    if not field_name:
        flash("Invalid therapist specialty.")
        return redirect(url_for("dashboard.dashboard_redirect"))

    # Get patients assigned to this therapist based on their specialty
    patients = Patient.query.filter(getattr(Patient, field_name) == current_user.id).all()

    # Handle form submission for creating a new support plan
    if request.method == 'POST':
        patient_id = request.form.get("patient_id")
        content = request.form.get("content")
        plan_date_str = request.form.get("plan_date")
        share_guardian = request.form.get("share_guardian") == "on"
        share_sw = request.form.get("share_sw") == "on"

        # Parse and validate the plan date
        try:
            plan_date = datetime.strptime(plan_date_str, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Invalid date format.")
            return redirect(url_for('dashboard.therapist_dashboard'))

        # Create and save the new support plan
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

    # Display the form for creating a new support plan
    return render_template('plan/submit_plan.html', patients=patients)

# AJAX endpoint for retrieving shared support plans based on patient and date
@plan_bp.route('/ajax_get_shared_support_plans')
@login_required
def ajax_get_shared_support_plans():
    # Determine access permissions based on user role
    role = current_user.role
    if role == "Guardian":
        share_field = SupportPlan.share_with_guardian
        patient_field = Patient.guardian_id
    elif role == "Support Worker":
        share_field = SupportPlan.share_with_sw
        patient_field = Patient.sw_id
    else:
        return jsonify({"error": "Unauthorized"}), 403

    # Get and validate request parameters
    patient_id = request.args.get('patient_id', type=int)
    date_str = request.args.get('plan_date')
    if not patient_id or not date_str:
        return jsonify({'error': 'Missing parameters'}), 400

    # Parse and validate the selected date
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Security check: ensure users can only access patients assigned to them
    patient = Patient.query.get(patient_id)
    if not patient or getattr(patient, patient_field.name) != current_user.id:
        return jsonify({'error': 'Unauthorized access to patient data'}), 403

    # Get all support plans shared with the current user role for the selected patient
    plans = SupportPlan.query.filter(
        SupportPlan.patient_id == patient_id,
        share_field == True
    ).all()

    # Filter plans to only include those matching the selected date
    filtered = [p for p in plans if p.date.date() == selected_date]

    # Group support plans by therapist specialty for organized display
    grouped = defaultdict(list)
    for plan in filtered:
        therapist = User.query.get(plan.therapist_id)
        if therapist and therapist.specialty:
            grouped[therapist.specialty].append(plan.content)

    return jsonify(grouped)

# AJAX endpoint for retrieving available dates with support plans for a patient
@plan_bp.route('/ajax_get_plan_dates_by_patient/<int:patient_id>')
@login_required
def ajax_get_plan_dates_by_patient(patient_id):
    # Determine access permissions based on user role
    role = current_user.role
    if role == "Guardian":
        share_field = SupportPlan.share_with_guardian
        patient_field = Patient.guardian_id
    elif role == "Support Worker":
        share_field = SupportPlan.share_with_sw
        patient_field = Patient.sw_id
    else:
        return jsonify({"error": "Unauthorized"}), 403

    # Security check: ensure users can only access patients assigned to them
    patient = Patient.query.get(patient_id)
    if not patient or getattr(patient, patient_field.name) != current_user.id:
        return jsonify({'error': 'Unauthorized access to patient data'}), 403

    # Get all dates that have support plans for this patient shared with current user
    plans = (
        SupportPlan.query
        .filter(SupportPlan.patient_id == patient_id, share_field == True)
        .with_entities(SupportPlan.date)
        .order_by(SupportPlan.date.desc())
        .all()
    )

    # Extract unique dates and format them as ISO strings
    unique_dates = sorted(list({p.date.date().isoformat() for p in plans}))
    return jsonify(unique_dates)
