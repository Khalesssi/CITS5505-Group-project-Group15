# This script deletes all records from the QuestionnaireAnswer table
from app import create_app
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer

# Create the Flask app instance
app = create_app()

# Perform deletion within the app context
with app.app_context():
    num_deleted = QuestionnaireAnswer.query.delete()
    db.session.commit()
    print(f"✅ Deleted {num_deleted} questionnaire records.")
