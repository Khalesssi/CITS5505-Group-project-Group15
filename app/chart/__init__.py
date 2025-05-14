from flask import Blueprint

# Create a Blueprint for the chart module with URL prefix '/chart'
chart_bp = Blueprint('chart', __name__, url_prefix='/chart',template_folder='templates')

# Import routes to register them with the Blueprint
from app.chart import routes