from app.extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone


class User(UserMixin, db.Model):
    """
    User model - Represents system users with different roles (guardian, support worker, therapist, admin)
    Inherits from UserMixin to provide Flask-Login functionality for authentication
    """
    # User identification
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Used for login and communication
    password_hash = db.Column(db.String(200), nullable=False)  # Stores the encrypted password hash
    
    # Role and specialty
    role = db.Column(db.String(50), nullable=False)  # User roles: 'Guardian', 'Support Worker', 'Therapist', 'Admin'
    specialty = db.Column(db.String(20))  # For therapists: 'Psychology', 'Physiotherapy', 'Occupational Therapy'
    
    # Personal and professional information
    full_name = db.Column(db.String(100))  # User's full name
    education = db.Column(db.String(200))  # Educational background
    experience = db.Column(db.String(300))  # Professional experience
    bio = db.Column(db.Text)  # Brief personal biography
    phone = db.Column(db.String(20))  # Contact phone number
    avatar_url = db.Column(db.String(200))  # URL to profile image
    
    # System tracking
    last_login = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))  # Timestamp of last login
