from app.extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)  # 用 password_hash 表示加密
    role = db.Column(db.String(50), nullable=False)  # 'guardian', 'sw', 'therapist', 'admin'
    specialty = db.Column(db.String(20))  # if therapist: 'psych', 'physio', 'ot'
    full_name = db.Column(db.String(100))
    education = db.Column(db.String(200))
    experience = db.Column(db.String(300))
    bio = db.Column(db.Text)
    phone = db.Column(db.String(20))
    register_time = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
