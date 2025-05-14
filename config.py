import os
# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Application configuration class
class Config:
    # Secret key used for session signing and CSRF protection
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-key"
    # Database connection URI (using SQLite in the local project directory)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "site.db")
    # Disable Flask-SQLAlchemy modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
