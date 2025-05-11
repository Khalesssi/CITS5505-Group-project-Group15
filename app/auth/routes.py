import re
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import auth_bp
from app.models import User
from app.extensions import db


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!")

            # ✅ 角色跳转
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

    return render_template("auth/login.html")  # ⬅ 确保路径是 auth 子目录


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))


@auth_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # ✅ 邮箱格式校验
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format.")
            return redirect(url_for('auth.register'))

        # ✅ 角色选择校验
        if not role:
            flash("Please select a role.")
            return redirect(url_for('auth.register'))

        # ✅ 重复邮箱检查
        if User.query.filter_by(email=email).first():
            flash("Email already registered.")
            return redirect(url_for('auth.register'))

        # ✅ 注册用户
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for('auth.login'))

    return render_template("auth/register.html")  # ⬅ 同样确保 auth 子模板