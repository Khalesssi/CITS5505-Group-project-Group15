from app import app
from flask import render_template

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/physio")
def physio_dashboard():
    return render_template("physio_dashboard.html")

@app.route("/ot")
def ot_dashboard():
    return render_template("ot_dashboard.html")

@app.route("/psych")
def psych_dashboard():
    return render_template("psych_dashboard.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin.html")

@app.route("/guardian")
def guardian_dashboard():
    return render_template("guardian.html")

@app.route("/supervisor")
def supervisor_dashboard():
    return render_template("supervisor.html")

@app.route("/support_worker")
def support_worker_dashboard():
    return render_template("support_worker.html")