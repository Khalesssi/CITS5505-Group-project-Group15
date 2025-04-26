from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__,
            template_folder="app/templates",     
            static_folder="app/static") 

app.secret_key = "your-secret-key"

# Setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Create user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Create data table
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        # Check if user exist
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!")
        return redirect(url_for("signup"))

    return render_template("signup.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user"] = user.email
            session["role"] = user.role
            flash("Login successful!")
            return redirect(url_for("login"))
        else:
            flash("Invalid credentials!")

    return render_template("login.html")

# Guardian route
@app.route('/guardian')
def guardian_dashboard():
    return render_template('guardian.html')

# Supervisor route
@app.route('/supervisor')
def supervisor_dashboard():
    return render_template('supervisor.html')

# Support Worker route
@app.route('/support_worker')
def support_worker_dashboard():
    return render_template('support_worker.html')

# Admin route
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')


# Physiotherapist dashboard
@app.route('/physio_dashboard')
def physio_dashboard():
    return render_template('physio_dashboard.html')

# Occupational Therapist dashboard
@app.route('/ot_dashboard')
def ot_dashboard():
    return render_template('ot_dashboard.html')

# Psychotherapist dashboard
@app.route('/psych_dashboard')
def psych_dashboard():
    return render_template('psych_dashboard.html')

# # guardian_updated dashboard
# @app.route('/guardian_updated')
# def guardian_updated():
#     return render_template('guardian_updated.html')

if __name__ == '__main__':
    app.run(debug=True)
