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


class Timesheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    workhours = db.Column(db.Numeric(5,1), nullable=False)
    description=db.Column(db.Text, nullable=True)    
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_updated = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('timesheets', lazy=True))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    subject = db.relationship('Subject', backref=db.backref('timesheets', lazy=True))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)
    task = db.relationship('Task', backref=db.backref('timesheets', lazy=True))

    def __repr__(self):
        if self.task:
            return f"Timesheet('{self.subject.name}', '{self.task.name}', '{self.date_created}', '{self.hours}')"
        else:
            return f"Timesheet('{self.subject.name}', '{self.date_created}', '{self.hours}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
