from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.routing import BaseConverter, ValidationError
from timetracker.config import Config

class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)
  app.url_map.converters['date'] = DateConverter

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  from timetracker.general.routes import general
  from timetracker.users.routes import users
  from timetracker.todos.routes import todos
  from timetracker.subjects.routes import subjects
  from timetracker.tasks.routes import tasks
  from timetracker.timesheets.routes import timesheets

  app.register_blueprint(general)
  app.register_blueprint(users)
  app.register_blueprint(todos)
  app.register_blueprint(subjects)
  app.register_blueprint(tasks)  
  app.register_blueprint(timesheets)

  return app	