# app/dashboard/__init__.py

from flask import Blueprint

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates')

from app.dashboard import routes  # 确保 routes 被导入
