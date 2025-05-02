from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timezone

app = create_app()

with app.app_context():
    # 插入用户
    guardian = User(email='guardian@outlook.com', password_hash=generate_password_hash('112233'), role='Guardian')
    sw = User(email='supportworker@outlook.com', password_hash=generate_password_hash('12345678'), role='Support Worker')
    physio = User(email='physio@example.com', password_hash=generate_password_hash('11223344'), role='Therapist', specialty='physio')
    ot = User(email='OT@outlook.com', password_hash=generate_password_hash('123456'), role='Therapist', specialty='ot')
    psych = User(email='psych@outlook.com', password_hash=generate_password_hash('7654321'), role='Therapist', specialty='psych')
    admin = User(email='admin@outlook.com', password_hash=generate_password_hash('13579'), role='Admin')

    db.session.add_all([guardian, sw, physio, ot, psych, admin])
    db.session.commit()

    # 插入一个病人
    patient = Patient(
        name="Test Patient",
        date_of_birth=date(1990, 1, 1),
        gender="Female",
        guardian_id=guardian.id,
        sw_id=sw.id,
        physio_id=physio.id,
        ot_id=ot.id,
        psych_id=psych.id,
        medical_info="Testing",
        notes="Dummy notes"
    )

    db.session.add(patient)
    db.session.commit()

    print(" Basic users and one patient inserted.")
