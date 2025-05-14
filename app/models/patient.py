from app.extensions import db
from datetime import date

class Patient(db.Model):
    """
    Patient model - Represents a healthcare patient with their basic information and associated healthcare professionals
    """
    # Primary identifier
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic patient information
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    # Relationships with healthcare professionals (foreign keys to User model)
    guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sw_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Support Worker assignment
    psych_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Psychologist assignment
    physio_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Physiotherapist assignment
    ot_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Occupational Therapist assignment

    # Additional patient details
    medical_info = db.Column(db.Text)  # Medical history and conditions
    notes = db.Column(db.Text)  # General notes about the patient
