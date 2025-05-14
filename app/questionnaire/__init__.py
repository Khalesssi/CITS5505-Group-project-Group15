# Questionnaire module - Handles daily patient assessments and report viewing functionality
from flask import Blueprint

# Create Blueprint for questionnaire module with URL prefix and template configuration
questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire', template_folder='templates')

# Import routes at the bottom to avoid circular dependencies
from app.questionnaire import routes