from app.extensions import db
from datetime import datetime

class QuestionnaireAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic info
    support_worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.now())

    # Question answer part
    q1_emotion_stable = db.Column(db.String(10))         # Yes/No
    q2_pain_present = db.Column(db.String(10))           # Yes/No
    q3_energy_level = db.Column(db.Integer)              # 1-5
    q4_food_intake = db.Column(db.String(20))            # Normal/Reduced/Excessive
    q5_daily_activities = db.Column(db.String(10))       # Yes/No
    q6_physical_training = db.Column(db.Integer)         # 0-100
    q7_post_exercise_pain = db.Column(db.Integer)        # 1-10
    q8_balance_score = db.Column(db.Integer)             # 1-5
    q9_self_care = db.Column(db.Integer)                 # 1-5
    q10_household_tasks = db.Column(db.String(30))       # Completed/Partially/Not

    q11_skill_learning = db.Column(db.String(10))        # Good/Average/Poor
    q12_emotional_fluctuations = db.Column(db.Integer)   # count
    q13_social_willingness = db.Column(db.Integer)       # 1-5
    q14_therapist_response = db.Column(db.Integer)       # 1-5
    q15_anxiety_depression = db.Column(db.String(10))    # Yes/No
