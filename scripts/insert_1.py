# This script populates the database with initial user and patient records for testing or demo purposes.
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from werkzeug.security import generate_password_hash
from datetime import date, datetime, timezone

# Create the Flask app instance
app = create_app()

# Run all operations within the application context
with app.app_context():
  # Optional: Uncomment these lines to clear existing data before inserting new ones
  # Patient.query.delete()
  # User.query.delete()
  # db.session.commit()

  # Create sample users for each system role (Guardian, Support Worker, Therapists, Admin)
  guardian = User(
    email='guardian@outlook.com',
    password_hash=generate_password_hash('112233'),
    role='Guardian',
    full_name='Grace Guardian',
    education='BA in Social Work',
    experience='5 years of experience in child care',
    bio='Guardian of a child with special needs.',
    phone='0400 000 001',
    avatar_url='/static/img/patient_photo.jpg',
    last_login=datetime.now(timezone.utc)
  )

  sw = User(
    email='supportworker@outlook.com',
    password_hash=generate_password_hash('12345678'),
    role='Support Worker',
    full_name='Sam Support',
    education='Certificate IV in Disability',
    experience='3 years in home support services',
    bio='Passionate about empowering people with disabilities.',
    phone='0400 000 002',
    avatar_url='/static/img/patient_photo.jpg',
    last_login=datetime.now(timezone.utc)
  )

  physio = User(
    email='physio@example.com',
    password_hash=generate_password_hash('11223344'),
    role='Therapist',
    specialty='physio',
    full_name='Phoebe Physio',
    education='Masters in Physiotherapy',
    experience='4 years in rehabilitation clinics',
    bio='Specializes in pediatric physical therapy.',
    phone='0400 000 003',
    avatar_url='/static/img/patient_photo.jpg',
    last_login=datetime.now(timezone.utc)
  )

  ot = User(
    email='OT@outlook.com',
    password_hash=generate_password_hash('123456'),
    role='Therapist',
    specialty='ot',
    full_name='Olivia OT',
    education='Masters in Occupational Therapy',
    experience='6 years in mental health and functional assessment',
    bio='Focuses on developing daily living skills.',
    phone='0400 000 004',
    avatar_url='/static/img/patient_photo.jpg',
    last_login=datetime.now(timezone.utc)
  )

  psych = User(
    email='psych@outlook.com',
    password_hash=generate_password_hash('7654321'),
    role='Therapist',
    specialty='psych',
    full_name='Paul Psychologist',
    education='Masters in Psychology',
    experience='10 years in child psychology',
    bio='Dedicated to understanding behavior and emotional development.',
    phone='0400 000 005',
    avatar_url='/static/img/patient_photo.jpg',
    last_login=datetime.now(timezone.utc)
  )

  admin = User(
    email='admin@outlook.com',
    password_hash=generate_password_hash('13579'),
    role='Admin',
    full_name='Alice Admin',
    education='BSc in Information Systems',
    experience='System administrator and coordinator',
    bio='Manages platform access and permissions.',
    phone='0400 000 006',
    avatar_url='/static/img/patient_photo.jpg',
    last_login=datetime.now(timezone.utc)
  )
  # Add all users to the session
  db.session.add_all([guardian, sw, physio, ot, psych, admin])
  db.session.commit()

  # Create two patient records linked to the users above
  patient = Patient(
    name="Test Patient",
    date_of_birth=date(2010, 5, 15),
    gender="Female",
    guardian_id=guardian.id,
    sw_id=sw.id,
    physio_id=physio.id,
    ot_id=ot.id,
    psych_id=psych.id,
    medical_info="Diagnosed with ADHD and mild autism spectrum disorder.",
    notes="Requires structured support, responds well to positive reinforcement."
  )
  patient2 = Patient(
    name="Test Patient 2",
    date_of_birth=date(2005, 6, 15),
    gender="Male",
    guardian_id=guardian.id,
    sw_id=sw.id,
    physio_id=physio.id,
    ot_id=ot.id,
    psych_id=psych.id,
    medical_info="Diagnosed with cerebral palsy and speech delay.",
    notes="Needs daily physiotherapy and speech reinforcement sessions."
  )


  # Add patients to the session and commit
  db.session.add(patient)
  db.session.add(patient2)
  db.session.commit()

  # Confirmation message
  print("one sets of users and 2 patients inserted successfully.")
