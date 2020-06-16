from datetime import datetime
from timetracker import db, login_manager
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False) 
	password = db.Column(db.String(32), nullable=False) 		

	def __repr__(self):
		return f"User '{self.username}'"

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.Text, nullable=False)
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	date_completed = db.Column(db.DateTime, nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	user = db.relationship('User', backref=db.backref('todos', lazy=True))	

	def __repr__(self):
		return f"Description: '{self.description}', Date: '{self.date_created}'"

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))