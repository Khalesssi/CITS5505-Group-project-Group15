# app/__init__.py

from flask import Flask,render_template
from config import Config
from config import DeploymentConfig
from app.extensions import db, login_manager, migrate, csrf 
from dotenv import load_dotenv
import os

load_dotenv()

def create_app(config_class=DeploymentConfig):
    app = Flask(__name__)
    # app.config.from_object(Config)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)
    csrf.init_app(app)

    # 注册蓝图

    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.questionnaire import questionnaire_bp
    from app.chart import chart_bp
    from app.plan import plan_bp
    # from app.share import share_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(chart_bp)
    app.register_blueprint(plan_bp)
    # # app.register_blueprint(share_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    from app import models

    return app