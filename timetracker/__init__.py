from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from timetracker.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	from timetracker.general.routes import general
	from timetracker.users.routes import users
	from timetracker.todos.routes import todos
	from timetracker.subjects.routes import subjects
	from timetracker.timesheets.routes import timesheets

	app.register_blueprint(general)
	app.register_blueprint(users)
	app.register_blueprint(todos)
	app.register_blueprint(subjects)
	app.register_blueprint(timesheets)

	return app	