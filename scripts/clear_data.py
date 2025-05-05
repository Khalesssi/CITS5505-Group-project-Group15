#this script is used to clear all data from the database
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.patient import Patient

app = create_app()

with app.app_context():
    # 注意：delete() 不会触发表级依赖检查，需手动控制顺序
    Patient.query.delete()
    User.query.delete()

    db.session.commit()
    print("All data cleared from User and Patient tables.")
