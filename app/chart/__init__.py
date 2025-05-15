from flask import Blueprint

# Define the blueprint for chart-related views.
# This blueprint handles routes for displaying data analytics and visualizations.
chart_bp = Blueprint('chart', __name__, url_prefix='/chart',template_folder='templates')

# Import route definitions to ensure they are registered with the blueprint.
from app.chart import routes