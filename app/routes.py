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
    # 这里是你想显示的病患列表，后续可以从数据库读取
    assigned_patients = ["Liu Yi", "Chen Er", "Zhao Wu", "Wang Fang"]
    return render_template("physio_dashboard.html", assigned_patients=assigned_patients)

@app.route("/guardian")
def guardian_dashboard():
    return render_template("guardian.html")