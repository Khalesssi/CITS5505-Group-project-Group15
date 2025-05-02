from flask import Blueprint

bp = Blueprint('chart', __name__, url_prefix='/chart')

@bp.route('/hello')
def hello():
    return "Hello from chart"
