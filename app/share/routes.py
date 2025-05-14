from flask import Blueprint # Import the Blueprint class from Flask to modularize routes

# Create a Blueprint for the 'share' module
# The routes in this file will be prefixed with '/share'
bp = Blueprint('share', __name__, url_prefix='/share')

# Define a simple route '/hello' under the 'share' blueprint
@bp.route('/hello')
def hello():
    return "Hello from share" # Return a test message when '/share/hello' is accessed
