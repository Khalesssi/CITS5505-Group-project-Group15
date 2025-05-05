from flask import Blueprint

bp = Blueprint('share', __name__, url_prefix='/share')

@bp.route('/hello')
def hello():
    return "Hello from share"
