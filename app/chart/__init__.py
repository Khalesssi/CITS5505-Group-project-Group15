from flask import Blueprint

chart_bp = Blueprint('chart', __name__, url_prefix='/chart',template_folder='templates')

from app.chart import routes