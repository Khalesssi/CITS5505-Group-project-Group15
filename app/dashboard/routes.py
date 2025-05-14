from flask import render_template
from collections import defaultdict
from app.dashboard import dashboard_bp 
from flask_login import login_required
from flask_login import current_user
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.models.user import User
from app.utils.role_mapping import role_to_patient_field    
from app.utils.role_mapping import specialty_to_field
from app.models.user import User
from flask import flash, redirect, url_for
# from app import db
from datetime import datetime
from flask import request
from app.extensions import db
from flask import render_template


# Guardian dashboard route - shows patients and their support plans
@dashboard_bp.route('/guardian')
@login_required
def guardian_dashboard():
    # Get patients bound to current guardian
    patients = Patient.query.filter_by(guardian_id=current_user.id).all()
    patient_ids = [p.id for p in patients]

    # Get support plans shared with guardian
    all_plans = SupportPlan.query.filter(
        SupportPlan.patient_id.in_(patient_ids),
        SupportPlan.share_with_guardian == True
    ).all()

    # Extract valid patients and dates
    plan_patient_ids = list({plan.patient_id for plan in all_plans})
    plan_dates = sorted(list({plan.date.date() for plan in all_plans}))

    # Process filter parameters from URL
    selected_patient_id = request.args.get('patient_id', type=int)
    selected_date_str = request.args.get('plan_date')
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else None

    # Only display plans when both patient and date are selected
    if selected_patient_id and selected_date:
        filtered_plans = [
            plan for plan in all_plans
            if plan.patient_id == selected_patient_id and plan.date.date() == selected_date
        ]
    else:
        filtered_plans = []

    # Group plans by therapist specialty for organized display
    grouped_plans = defaultdict(list)
    for plan in filtered_plans:
        therapist = User.query.get(plan.therapist_id)
        if therapist and therapist.specialty:
            grouped_plans[therapist.specialty].append(plan)

    return render_template(
        'dashboard/guardian.html',
        patients=patients,
        grouped_plans=grouped_plans,
        plan_patient_ids=plan_patient_ids,
        plan_dates=plan_dates,
        selected_patient_id=selected_patient_id,
        selected_date_str=selected_date_str
    )

# Support Worker dashboard route - shows assigned patients and their support plans
@dashboard_bp.route('/sw')
@login_required
def sw_dashboard():
    # Get patients bound to current support worker
    patients = Patient.query.filter_by(sw_id=current_user.id).all()
    patient_ids = [p.id for p in patients]

    # Get support plans shared with support worker
    all_plans = SupportPlan.query.filter(
        SupportPlan.patient_id.in_(patient_ids),
        SupportPlan.share_with_sw == True
    ).all()

    # Extract valid patients and dates
    plan_patient_ids = list({plan.patient_id for plan in all_plans})
    plan_dates = sorted(list({plan.date.date() for plan in all_plans}))

    # Process filter parameters from URL
    selected_patient_id = request.args.get('patient_id', type=int)
    selected_date_str = request.args.get('plan_date')
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else None

    # Only display plans when both patient and date are selected
    if selected_patient_id and selected_date:
        filtered_plans = [
            plan for plan in all_plans
            if plan.patient_id == selected_patient_id and plan.date.date() == selected_date
        ]
    else:
        filtered_plans = []

    # Group plans by therapist specialty for organized display
    grouped_plans = defaultdict(list)
    for plan in filtered_plans:
        therapist = User.query.get(plan.therapist_id)
        if therapist and therapist.specialty:
            grouped_plans[therapist.specialty].append(plan)

    return render_template(
        'dashboard/sw.html',  # Shared template with guardian view
        patients=patients,
        grouped_plans=grouped_plans,
        plan_patient_ids=plan_patient_ids,
        plan_dates=plan_dates,
        selected_patient_id=selected_patient_id,
        selected_date_str=selected_date_str
    )


# Therapist dashboard route - shows patients assigned to the therapist based on specialty
@dashboard_bp.route('/therapist')
@login_required
def therapist_dashboard():
    # Map therapist specialty to corresponding patient field (psych_id, physio_id, ot_id)
    field = specialty_to_field.get(current_user.specialty)
    # Get patients assigned to this therapist
    patients = Patient.query.filter(getattr(Patient, field) == current_user.id).all() if field else []
    return render_template('dashboard/therapist.html', patients=patients)


# Admin dashboard route - displays user management interface
@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    # Verify user has admin role
    if current_user.role != "Admin":
        flash("Access denied.")
        return redirect(url_for("auth.login"))
    
    # Get all users for management
    users = User.query.all()
    return render_template('dashboard/admin.html', users=users)

# Role-based dashboard redirect - routes users to appropriate dashboard
@dashboard_bp.route('/redirect')
@login_required
def dashboard_redirect():
    role = current_user.role
    if role == "Support Worker":
        return redirect(url_for("dashboard.sw_dashboard"))
    elif role == "Guardian":
        return redirect(url_for("dashboard.guardian_dashboard"))
    elif role == "Therapist":
        return redirect(url_for("dashboard.therapist_dashboard"))
    elif role == "Admin":
        return redirect(url_for("dashboard.admin_dashboard"))
    else:
        flash("No dashboard defined for this role.")
        return redirect(url_for("auth.login"))



# Commented-out original simple route definitions
# @dashboard_bp.route('/guardian')
# @login_required
# def guardian_dashboard():
#     return render_template('dashboard/guardian.html')

# @dashboard_bp.route('/sw')
# @login_required
# def sw_dashboard():
#     return render_template('dashboard/sw.html')

# @dashboard_bp.route('/therapist')
# @login_required
# def therapist_dashboard():
#     return render_template('dashboard/therapist.html')

# @dashboard_bp.route('/admin')
# @login_required
# def admin_dashboard():
#     return render_template('dashboard/admin.html')

