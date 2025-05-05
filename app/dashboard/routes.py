from flask import render_template
from app.dashboard import dashboard_bp 
from flask_login import login_required
from flask_login import current_user
from app.models.patient import Patient
from app.utils.role_mapping import role_to_patient_field


@dashboard_bp.route('/guardian')
@login_required
def guardian_dashboard():
    return render_template('dashboard/guardian.html')

@dashboard_bp.route('/sw')
@login_required
def sw_dashboard():
    return render_template('dashboard/sw.html')

@dashboard_bp.route('/therapist')
@login_required
def therapist_dashboard():
    return render_template('dashboard/therapist.html')

@dashboard_bp.route('/admin')
@login_required
def admin_dashboard():
    return render_template('dashboard/admin.html')

