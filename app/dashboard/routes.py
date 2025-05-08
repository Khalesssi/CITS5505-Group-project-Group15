# app/dashboard/routes.py

from flask import render_template
from app.dashboard import bp 

from flask_login import login_required

from app.models import Patient


@bp.route('/guardian')
@login_required
def guardian_dashboard():
    return render_template('dashboard/guardian.html')

@bp.route('/sw')
@login_required
def sw_dashboard():
    # 查询 Patient
    patients = Patient.query.all()

    return render_template('dashboard/sw.html',patients=[{
            'id': patient.id, 'name': patient.name
        } for patient in patients])

@bp.route('/therapist')
@login_required
def therapist_dashboard():
    return render_template('dashboard/therapist.html')

@bp.route('/admin')
@login_required
def admin_dashboard():
    return render_template('dashboard/admin.html')