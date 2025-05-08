# app/__init__.py

from flask import Flask,render_template
from config import Config
from app.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    migrate.init_app(app, db)

    # 注册蓝图

    from app.auth.routes import bp as auth_bp
    from app.dashboard.routes import bp as dashboard_bp
    from app.questionnaire.routes import bp as questionnaire_bp
    from app.chart.routes import bp as chart_bp
    from app.plan.routes import bp as plan_bp
    from app.share.routes import bp as share_bp

    app.register_blueprint(auth_bp)
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(chart_bp)
    app.register_blueprint(plan_bp)
    app.register_blueprint(share_bp)

    @app.route("/")
    def home():
        return render_template("home.html")

    from app import models

    return app
