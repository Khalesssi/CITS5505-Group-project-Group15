from app import db
from datetime import datetime, date

# ---------------------- Create database ------------------------

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # User id
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(50), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)  # Default login time is now

# Patient table
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Patient ID
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the Gardian
    medical_info = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

# Assignment table
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # SW or Therapist
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

#Questionnaire table
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    support_worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)

    # Common answer--to all therapists
    q1_emotion_stable = db.Column(db.String(10))
    q2_pain_present = db.Column(db.String(10))
    q3_energy_level = db.Column(db.Integer)
    q4_food_intake = db.Column(db.String(20))
    q5_daily_activity = db.Column(db.String(10))

    # Physiotherapist
    q6_physio_completion = db.Column(db.Integer)
    q7_post_exercise_pain = db.Column(db.Integer)
    q8_balance_score = db.Column(db.Integer)

    # Occupational Therapist
    q9_selfcare_willingness = db.Column(db.Integer)
    q10_household_task = db.Column(db.String(20))
    q11_skill_learning = db.Column(db.String(20))

    # Psychotherapist
    q12_emotion_fluctuation = db.Column(db.Integer)
    q13_social_willingness = db.Column(db.Integer)
    q14_therapy_response = db.Column(db.Integer)
    q15_anxiety_depression = db.Column(db.String(10))

    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
