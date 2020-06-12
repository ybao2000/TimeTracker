from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cdcd1a66-9d2d-11ea-bb37-0242ac130002'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from timetracker import routes	# added after class 5