from flask import Blueprint

bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')

@bp.route('/hello')
def hello():
    return "Hello from questionnaire"
