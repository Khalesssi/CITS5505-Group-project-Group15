from app.extensions import db
from datetime import date

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sw_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Bind Support Worker 
    psych_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    physio_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ot_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    medical_info = db.Column(db.Text)
    notes = db.Column(db.Text)
