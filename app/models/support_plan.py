from app.extensions import db
from datetime import datetime

class SupportPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    share_with_guardian = db.Column(db.Boolean, default=False)
    share_with_sw = db.Column(db.Boolean, default=False)
