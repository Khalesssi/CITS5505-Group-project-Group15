# run.py

# Import the Flask application factory
from app import create_app

# Create the Flask app instance
app = create_app()

# Entry point of the application
# Runs the app in debug mode (recommended only for development)
if __name__ == '__main__':
    app.run(debug=True)
