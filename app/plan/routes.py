from flask import Blueprint

bp = Blueprint('plan', __name__, url_prefix='/plan')

@bp.route('/hello')
def hello():
    return "Hello from plan"
