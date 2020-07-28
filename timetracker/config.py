import os

class Config:
    SECRET_KEY = "286f8315db7facc8903fd77bd5315c19"
    SQLALCHEMY_DATABASE_URI = "sqlite:///timetracker.db"
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')