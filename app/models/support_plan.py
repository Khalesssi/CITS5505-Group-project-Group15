from app.extensions import db
from datetime import datetime

class SupportPlan(db.Model):
    """
    SupportPlan model - Represents a therapy support plan created by therapists for patients
    Contains instructions and guidance that can be optionally shared with guardians and support workers
    """
    # Plan identification
    id = db.Column(db.Integer, primary_key=True)
    
    # Relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)  # Patient receiving the support plan
    therapist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Therapist who created the plan
    
    # Plan details
    content = db.Column(db.Text, nullable=False)  # The actual content/instructions of the support plan
    date = db.Column(db.DateTime, nullable=False)  # When the support plan was created

    # Sharing permissions
    share_with_guardian = db.Column(db.Boolean, default=False)  # Whether the plan is visible to the patient's guardian
    share_with_sw = db.Column(db.Boolean, default=False)  # Whether the plan is visible to support workers
