from app.extensions import db
from datetime import datetime

class SupportPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Primary key for the support plan record
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    # ID of the patient this plan is associated with
    therapist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # ID of the therapist who created the plan
    content = db.Column(db.Text, nullable=False)
    # Detailed content of the support plan
    date = db.Column(db.DateTime, nullable=False)
    # Timestamp of when the plan was created or last updated

    share_with_guardian = db.Column(db.Boolean, default=False)
    # Flag indicating whether this plan is shared with the guardian
    share_with_sw = db.Column(db.Boolean, default=False)
    # Flag indicating whether this plan is shared with the support worker
