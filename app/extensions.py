# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize Flask extensions (without attaching to app yet)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


from app.models import User

# Callback used by Flask-Login to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))