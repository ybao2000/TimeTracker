from datetime import datetime
from timetracker import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False) 
	password = db.Column(db.String(64), nullable=False) 		

	def __repr__(self):
		return f"User '{self.username}'"

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(256), nullable=False)
	description = db.Column(db.Text, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_completed = db.Column(db.DateTime, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('todos', lazy=True))	

	def __repr__(self):
		return f"Description: '{self.description}', Date: '{self.date_created}'"

class Subject(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(126), nullable=False)
  description = db.Column(db.Text, nullable=False)
  date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  active = db.Column(db.Boolean, nullable=False, default=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  user = db.relationship('User', backref=db.backref('subjects', lazy=True))

  def __repr__(self):
  		return f"Name: '{self.name}', Date: '{self.date_created}'"

class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(126), nullable=False)
  description = db.Column(db.Text, nullable=False)
  date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  active = db.Column(db.Boolean, nullable=False, default=True)

  subject_id  = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
  subject = db.relationship('Subject', backref=db.backref('tasks', lazy=True))

  def __repf__(self):
  		return f"Name: '{self.name}', Date: '{self.date_created}'"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))