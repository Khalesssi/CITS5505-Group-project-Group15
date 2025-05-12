from app import create_app
from app.extensions import db
from app.models.questionnaire import QuestionnaireAnswer

app = create_app()

with app.app_context():
    num_deleted = QuestionnaireAnswer.query.delete()
    db.session.commit()
    print(f"✅ Deleted {num_deleted} questionnaire records.")
