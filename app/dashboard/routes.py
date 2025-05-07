from flask import render_template
from app.dashboard import dashboard_bp 
from flask_login import login_required
from flask_login import current_user
from app.models.patient import Patient
from app.utils.role_mapping import role_to_patient_field    
from app.utils.role_mapping import specialty_to_field
from app.models.user import User
from flask import flash, redirect, url_for
# from app import db

@dashboard_bp.route('/guardian')
@login_required
def guardian_dashboard():
    patients = Patient.query.filter_by(guardian_id=current_user.id).all()
    return render_template('dashboard/guardian.html', patients=patients)


@dashboard_bp.route('/sw')
@login_required
def sw_dashboard():
    patients = Patient.query.filter_by(sw_id=current_user.id).all()
    return render_template('dashboard/sw.html', patients=patients)


@dashboard_bp.route('/therapist')
@login_required
def therapist_dashboard():
    field = specialty_to_field.get(current_user.specialty)  # psych_id / physio_id / ot_id
    patients = Patient.query.filter(getattr(Patient, field) == current_user.id).all() if field else []
    return render_template('dashboard/therapist.html', patients=patients)


@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != "Admin":
        flash("Access denied.")
        return redirect(url_for("auth.login"))
    
    users = User.query.all()
    return render_template('dashboard/admin.html', users=users)

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

