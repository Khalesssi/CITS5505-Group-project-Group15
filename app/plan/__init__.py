from flask import Blueprint

plan_bp = Blueprint('plan', __name__, template_folder='templates',url_prefix='/plan')

from app.plan import routes  # Must be imported below to avoid circular dependency
