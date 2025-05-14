# Plan module - Handles support plan creation and sharing functionality
from flask import Blueprint

plan_bp = Blueprint('plan', __name__, template_folder='templates',url_prefix='/plan')

from app.plan import routes  # Must import at the bottom to avoid circular dependencies
