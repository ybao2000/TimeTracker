from flask import render_template, Blueprint, flash, url_for, request, abort, redirect
from flask_login import current_user, login_required
from timetracker import db
from timetracker.models import Subject, Task
from timetracker.subjects.forms import SubjectForm

subjects = Blueprint('subjects', __name__)

@subjects.route('/subjects_tasks')
def subjects_tasks():
  subjects = Subject.query.filter_by(user_id=current_user.id).order_by(Subject.name).all()
  return render_template('subjects_tasks.html', subjects=subjects, title="Subjects & Tasks")  

@subjects.route('/subjects/new', methods=['GET', 'POST'])
@login_required
def new_subject():
  form = SubjectForm()
  if form.validate_on_submit():  # POST only
    subject = Subject.query.filter_by(user_id=current_user.id, name=form.name.data).first()
    if subject:
      flash(f"Subject '{form.name.data} already exists.", "danger")
    else:
      subject = Subject(name=form.name.data, description=form.description.data, user=current_user)
      db.session.add(subject)
      db.session.commit()
      flash(f"Subject '{form.name.data} has been created", "success")
      return redirect(url_for('subjects.subjects_tasks'))
  elif request.method=='GET':
    form.active.data = True

  return render_template('edit_subject.html', title="New Subject", form=form)

@subjects.route('/subjects/<int:subject_id>')
def subject(subject_id):
  pass