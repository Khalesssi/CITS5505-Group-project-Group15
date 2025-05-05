from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from app.auth import routes  # 确保 routes.py 被加载



