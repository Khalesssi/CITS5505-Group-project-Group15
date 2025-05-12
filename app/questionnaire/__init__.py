from flask import Blueprint

questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire', template_folder='templates')

from app.questionnaire import routes