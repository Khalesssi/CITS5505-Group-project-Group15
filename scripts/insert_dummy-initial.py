import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from werkzeug.security import generate_password_hash
from datetime import date

app = create_app()

with app.app_context():
    # Add users: Only insert user when not exist
    def safe_add_user(email, password, role, specialty=None):
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(email=email, password_hash=generate_password_hash(password), role=role, specialty=specialty)
            db.session.add(user)
            db.session.commit()
        return user

    guardian = safe_add_user('guardian@outlook.com', '112233', 'Guardian')
    sw = safe_add_user('supportworker@outlook.com', '12345678', 'Support Worker')
    physio = safe_add_user('physio@example.com', '11223344', 'Therapist', specialty='physio')
    ot = safe_add_user('OT@outlook.com', '123456', 'Therapist', specialty='ot')
    psych = safe_add_user('psych@outlook.com', '7654321', 'Therapist', specialty='psych')
    admin = safe_add_user('admin@outlook.com', '13579', 'Admin')

    # Add patients: Only insert patients when not exist
    def safe_add_patient(name, dob, gender, notes, medical_info):
        if not Patient.query.filter_by(name=name).first():
            patient = Patient(
                name=name,
                date_of_birth=dob,
                gender=gender,
                guardian_id=guardian.id,
                sw_id=sw.id,
                physio_id=physio.id,
                ot_id=ot.id,
                psych_id=psych.id,
                medical_info=medical_info,
                notes=notes
            )
            db.session.add(patient)
            db.session.commit()
            print(f" Added patient: {name}")
        else:
            print(f" Patient '{name}' already exists, skipping.")

    safe_add_patient(
        name="Test Patient",
        dob=date(1990, 1, 1),
        gender="Female",
        medical_info="Testing",
        notes="Dummy notes"
    )

    safe_add_patient(
        name="Test2 Patient",
        dob=date(1985, 5, 5),
        gender="Male",
        medical_info="Additional dummy patient",
        notes="Second dummy"
    )

    print("Dummy users and patients inserted without duplication.")

