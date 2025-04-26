# import part 
import re
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Flask setup
app = Flask(__name__,
            template_folder="app/templates",
            static_folder="app/static")
app.secret_key = "your-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Create database 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    role = db.Column(db.String(50), nullable=False)

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
@app.route('/guardian')
def guardian_dashboard():
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
@app.route('/admin')
def admin_dashboard():
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

# start app
if __name__ == "__main__":
    app.run(debug=True)
