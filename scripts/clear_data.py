from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient
from app.models.support_plan import SupportPlan
from app.models.questionnaire import QuestionnaireAnswer

app = create_app()

with app.app_context():
    try:
        # 先清空依赖项多的表，再清空主表
        QuestionnaireAnswer.query.delete()
        # SupportPlan.query.delete()
        # Patient.query.delete()
        # User.query.delete()

        db.session.commit()
        print("All data cleared successfully.")
    except Exception as e:
        db.session.rollback()
        print(" Error occurred while clearing data:", e)
