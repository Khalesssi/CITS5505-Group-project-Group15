from flask import Blueprint

# Define the authentication blueprint.
# This blueprint handles routes related to login, registration, and logout.
auth_bp = Blueprint('auth', __name__, template_folder='templates')

# Import routes to register them with the blueprint.
# This ensures the associated route handlers are loaded when the app starts.
from app.auth import routes  



