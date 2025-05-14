#this script is used to clear all data from the database
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient

# Create the Flask app instance
app = create_app()

# Run the database operations within the application context
with app.app_context():
    # Warning: delete() does not trigger table-level dependency checks.
    # You must manually delete tables in the correct order to avoid foreign key issues.

    Patient.query.delete()
    User.query.delete()

    db.session.commit()
    print("All data cleared from User and Patient tables.")
