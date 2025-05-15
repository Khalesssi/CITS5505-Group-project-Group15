from flask import Blueprint

# Create a Blueprint for the questionnaire module
# This Blueprint handles all routes prefixed with '/questionnaire'
# and uses the 'templates' folder for rendering templates.
questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire', template_folder='templates')

# Import routes to register them with the Blueprint
from app.questionnaire import routes