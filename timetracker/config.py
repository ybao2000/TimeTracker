import os

class Config:
  SECRET_KEY = "286f8315db7facc8903fd77bd5315c19"
  # SQLALCHEMY_DATABASE_URI = "sqlite:///timetracker.db"
  SQLALCHEMY_DATABASE_URI = "postgres://dwfuixotxjoufa:efffa058c0f8ec22691758dfc6b9d02624d9a9cddf32e2671dc1705736c396c7@ec2-3-215-83-17.compute-1.amazonaws.com:5432/d8nj4f0mf5g1mm"
  MAIL_SERVER = 'smtp.gmail.com'
  MAIL_PORT = 587
  MAIL_USE_TLS = True
  MAIL_USERNAME = os.environ.get('EMAIL_USER')
  MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')