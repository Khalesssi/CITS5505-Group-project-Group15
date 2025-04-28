# import part 
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date


# Flask setup
app = Flask(__name__,
            template_folder="app/templates",
            static_folder="app/static")
app.secret_key = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# ---------------------- Create database ------------------------

# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # User id
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(50), nullable=False)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)  # Default login time is now

# Patient table
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Patient ID
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    guardian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to the Gardian
    medical_info = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

# Assignment table
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # SW or Therapist
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return render_template("home.html")

# ---------------------- Register ------------------------
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        # 1. Check email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format. Please enter a valid email.")
            return redirect(url_for('register'))

        # 2. Check role selection
        if not role or role == "":
            flash("Please select a role!")
            return redirect(url_for('register'))

        # 3. Check if already registed
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User already registered! Please login.")
            return redirect(url_for('register'))

        # 4. Password Encryption
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.")
        return redirect(url_for('login'))

    return render_template('register.html')

# ---------------------- Log in ------------------------
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # Login successfully, create session
            session['user_id'] = user.id
            session['email'] = user.email
            session['role'] = user.role
            flash("Login successful!")

            # If role is support worker
            if user.role == "Support Worker":
                return redirect(url_for('support_worker_page'))
            elif user.role == "Physiotherapist":
                return redirect(url_for('physio_dashboard'))
            elif user.role == "Psychotherapist":
                return redirect(url_for('psych_dashboard'))
            elif user.role == "Supervisor":
                return redirect(url_for('supervisor_dashboard'))
            elif user.role == "Occupational Therapist":
                return redirect(url_for('ot_dashboard'))
            elif user.role == "Guardian":
                return redirect(url_for('guardian_dashboard'))
            elif user.role == "Admin":
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))  
        else:
            # Login fail
            flash("Invalid email or password.")
            return redirect(url_for('login'))

    # Render the login page via a GET request
    return render_template('login.html')




# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))


# Guardian route
@app.route('/guardian_dashboard')
def guardian_dashboard():
    if 'user_id' not in session or session.get('role') != "Guardian":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('guardian.html')


# Supervisor route
@app.route('/supervisor_dashboard')
def supervisor_dashboard():
    if 'user_id' not in session or session.get('role') != "Supervisor":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('supervisor.html')

# Support Worker route
@app.route('/support_worker')
def support_worker_page():
    if 'user_id' not in session or session.get('role') != "Support Worker":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('support_worker.html')

# Admin route
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != "Admin":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('admin.html')



# Physiotherapist dashboard
@app.route('/physio_dashboard')
def physio_dashboard():
    if 'user_id' not in session or session.get('role') != "Physiotherapist":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('physio_dashboard.html')

# Occupational Therapist dashboard
@app.route('/ot_dashboard')
def ot_dashboard():
    if 'user_id' not in session or session.get('role') != "Occupational Therapist":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('ot_dashboard.html')

# Psychotherapist dashboard
@app.route('/psych_dashboard')
def psych_dashboard():
    if 'user_id' not in session or session.get('role') != "Psychotherapist":
        flash("Access denied.")
        return redirect(url_for('login'))
    return render_template('psych_dashboard.html')

# # guardian_updated dashboard
# @app.route('/guardian_updated')
# def guardian_updated():
#     return render_template('guardian_updated.html')

# Test data

# Test user data
from werkzeug.security import generate_password_hash
from run import db, User
from run import app  # 确保导入了app对象

with app.app_context():

# Test user data

#     if User.query.first() is None:
#         guardian = User(
#         email='guardian@outlook.com',
#         password=generate_password_hash('112233'),
#         role='Guardian'
#     )
#         support_worker = User(
#         email='supportworker@outlook.com',
#         password=generate_password_hash('12345678'),
#         role='Support Worker'
#     )
#         physiotherapist = User(
#         email='physio@example.com',
#         password=generate_password_hash('11223344'),
#         role='Physiotherapist'
#     )
#         ot = User(
#         email='OT@outlook.com',
#         password=generate_password_hash('123456'),
#         role='Occupational Therapist'
#     )
#         psychotherapist = User(
#         email='psych@outlook.com',
#         password=generate_password_hash('7654321'),
#         role='Psychotherapist'
#     )
#         admin = User(
#         email='admin@outlook.com',
#         password=generate_password_hash('13579'),
#         role='Admin'
#     )

#         db.session.add_all([guardian, support_worker, physiotherapist, ot, psychotherapist, admin])
#         db.session.commit()
#         print('Successfully add user!')
#     else:
#         print('Users exist!')

# from run import Patient

# with app.app_context():
#     if Patient.query.first() is None:
#         patient1 = Patient(
#             name="Alice Johnson",
#             date_of_birth=date(1990, 5, 10),
#             gender="Female",
#             guardian_id=1,
#             medical_info="Loss of coordination",
#             notes="Needs inhaler during exercise."
#         )
#         patient2 = Patient(
#             name="Bob Smith",
#             date_of_birth=date(1985, 8, 20),
#             gender="Male",
#             guardian_id=1,
#             medical_info="Delusions",
#             notes="Requires insulin shots."
#         )
#         patient3 = Patient(
#             name="Charlie Lee",
#             date_of_birth=date(2000, 3, 5),
#             gender="Male",
#             guardian_id=1,
#             medical_info="Vision loss",
#             notes="Healthy"
#         )
#         patient4 = Patient(
#             name="Diana Moore",
#             date_of_birth=date(1995, 12, 12),
#             gender="Female",
#             guardian_id=1,
#             medical_info="Depression",
#             notes="Avoid certain foods."
#         )
#         patient5 = Patient(
#             name="Ethan Brown",
#             date_of_birth=date(1992, 9, 9),
#             gender="Male",
#             guardian_id=1,
#             medical_info="Epilepsy",
#             notes="Takes medication daily."
#         )

#         db.session.add_all([patient1, patient2, patient3, patient4, patient5])
#         db.session.commit()
#         print('Successfully add patients!')
#     else:
#         print('Patients exist!')

# Test data for assignment arrangement

    # from run import Assignment
    # with app.app_context():
    #     if Assignment.query.first() is None:
    #         assignment1 = Assignment(user_id=2, patient_id=1)  # Support Worker has patient 1&2
    #         assignment2 = Assignment(user_id=2, patient_id=2)  
        
    #         assignment3 = Assignment(user_id=3, patient_id=2)  # Physiotherapist has patient 2&3
    #         assignment4 = Assignment(user_id=3, patient_id=3)  
        
    #         assignment5 = Assignment(user_id=4, patient_id=4)  # OT has patient 4&5
    #         assignment6 = Assignment(user_id=4, patient_id=5)  
        
    #         assignment7 = Assignment(user_id=5, patient_id=1)  # Psychotherapist has patient 1&5
    #         assignment8 = Assignment(user_id=5, patient_id=5)  

    #         db.session.add_all([assignment1, assignment2, assignment3, assignment4, assignment5, assignment6, assignment7, assignment8])
    #         db.session.commit()
    #         print('Successfully add assignment!')
    #     else:
    #         print('Assignment exist!')




# start app
    if __name__ == "__main__":
        app.run(debug=True)
