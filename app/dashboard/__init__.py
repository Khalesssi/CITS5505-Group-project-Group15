# app/dashboard/__init__.py

from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')

from app.dashboard import routes  # Ensure routes are imported
