import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'supersecretkey123'

    # Database (SQLite)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security settings
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False