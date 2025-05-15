from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.auth import auth_bp
from app.models import User
from app.extensions import db
from app.forms.auth_forms import LoginForm
import re
from flask import request
from werkzeug.security import generate_password_hash
from app.forms.auth_forms import RegisterForm



# Authentication Routes: Login, Logout, Register
@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!")

            role = user.role
            if role == "Support Worker":
                return redirect(url_for("dashboard.sw_dashboard"))
            elif role == "Guardian":
                return redirect(url_for("dashboard.guardian_dashboard"))
            elif role == "Therapist":
                return redirect(url_for("dashboard.therapist_dashboard"))
            elif role == "Admin":
                return redirect(url_for("dashboard.admin_dashboard"))
            else:
                flash("Unknown role.")
                return redirect(url_for("auth.login"))

        flash("Invalid credentials.")
        return redirect(url_for("auth.login"))
    # Render login page
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        role = form.role.data

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.")
            return redirect(url_for('auth.register'))
        
        # Ensure role is selected
        if not role:
            flash("Please select a role.")
            return redirect(url_for('auth.register'))
        
        # Check if email is already registered
        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for('auth.register'))

        # Create and add new user
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('auth.login'))

    # Render registration page
    return render_template("auth/register.html", form=form)
