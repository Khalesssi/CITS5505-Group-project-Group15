# app/auth/routes.py
import re
from flask import render_template, request, redirect, url_for, flash, session
from app.auth import bp
from app.models import User
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from app import db
from flask_login import login_user
from flask_login import logout_user


# @bp.route('/login', methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
#         user = User.query.filter_by(email=email).first()

#         if user and check_password_hash(user.password_hash, password):
#             session["user_id"] = user.id
#             session["role"] = user.role
#             flash("Login successful!")

            
#             if user.role == "Support Worker":
#                 return redirect(url_for("dashboard.sw_dashboard"))
#             elif user.role == "Guardian":
#                 return redirect(url_for("dashboard.guardian_dashboard"))
#             elif user.role == "Admin":
#                 return redirect(url_for("dashboard.admin_dashboard"))
#             elif user.role == "Therapist":
#                 return redirect(url_for("dashboard.therapist_dashboard"))
#             else:
#                 flash("Unknown role.")
#                 return redirect(url_for("auth.login"))

#         flash("Invalid credentials.")
#         return redirect(url_for("auth.login"))

#     return render_template("auth/login.html")



@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # ✅ 取代手动设置 session
            flash("Login successful!")

            # 用 user.role 跳转
            if user.role == "Support Worker":
                return redirect(url_for("dashboard.sw_dashboard"))
            elif user.role == "Guardian":
                return redirect(url_for("dashboard.guardian_dashboard"))
            elif user.role == "Admin":
                return redirect(url_for("dashboard.admin_dashboard"))
            elif user.role == "Therapist":
                return redirect(url_for("dashboard.therapist_dashboard"))
            else:
                flash("Unknown role.")
                return redirect(url_for("auth.login"))

        flash("Invalid credentials.")
        return redirect(url_for("auth.login"))

    return render_template("auth/login.html")



@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))


@bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # 1. Check email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format. Please enter a valid email.")
            return redirect(url_for('auth.register'))

        # 2. Check role selection
        if not role or role == "":
            flash("Please select a role!")
            return redirect(url_for('auth.register'))

        # 3. Check if already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already registered! Please login.")
            return redirect(url_for('auth.register'))

        # 4. Create new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')  # 确保路径正确