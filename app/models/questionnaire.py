from app.extensions import db
from datetime import datetime
from datetime import date

class QuestionnaireAnswer(db.Model):
    """
    QuestionnaireAnswer model - Stores patient assessment data collected by support workers
    This captures various aspects of patient health and well-being through standardized questions
    """
    id = db.Column(db.Integer, primary_key=True)
    
    # Questionnaire metadata
    support_worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Support worker who completed the assessment
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)  # Patient being assessed
    report_date = db.Column(db.Date, nullable=False, default=date.today)  # Date when assessment was completed

    # Emotional and physical health assessment
    q1_emotion_stable = db.Column(db.String(10))         # Yes-1/No-0: Patient's emotional stability
    q2_pain_present = db.Column(db.String(10))           # Yes-1/No-0: Presence of physical pain
    q3_energy_level = db.Column(db.Integer)              # 1-5: Energy level (1=very low, 5=excellent)
    q4_food_intake = db.Column(db.String(20))            # Normal-1/Reduced-3/Excessive-5: Eating patterns
    q5_daily_activities = db.Column(db.String(10))       # Yes-1/No-0: Completed daily activities

    # Physical therapy and exercise assessment
    q6_physical_training = db.Column(db.Integer)         # 0-100: Percentage of prescribed exercise completion
    q7_post_exercise_pain = db.Column(db.Integer)        # 1-10: Pain level after physical exercises
    q8_balance_score = db.Column(db.Integer)             # 1-5: Balance assessment (1=poor, 5=excellent)
    
    # Independent living skills assessment
    q9_self_care = db.Column(db.Integer)                 # 1-5: Self-care ability (bathing, dressing, etc.)
    q10_household_tasks = db.Column(db.String(30))       # Completed-5/Partially-3/Not-0: Household task completion

    # Cognitive and social assessment
    q11_skill_learning = db.Column(db.String(10))        # Good-5/Average-3/Poor-1: New skill acquisition
    q12_emotional_fluctuations = db.Column(db.Integer)   # Count of significant emotional episodes
    q13_social_willingness = db.Column(db.Integer)       # 1-5: Willingness to engage socially
    q14_therapist_response = db.Column(db.Integer)       # 1-5: Response to therapist instructions
    q15_anxiety_depression = db.Column(db.String(10))    # Yes-1/No-0: Signs of anxiety or depression
