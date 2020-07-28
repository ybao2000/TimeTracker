from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from timetracker import db
from timetracker.models import Subject, Task, Timesheet
from timetracker.subjects.forms import SubjectForm

subjects = Blueprint('subjects', __name__)

@subjects.route('/subjects_tasks')
@login_required
def subjects_tasks():
    subjects = Subject.query.filter_by(user_id=current_user.id).order_by(Subject.name).all()
    return render_template('subjects_tasks.html', subjects=subjects, title='Subjects & Tasks')

@subjects.route('/subject/new', methods=['GET', 'POST'])
@login_required
def new_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject.query.filter_by(user_id=current_user.id, name=form.name.data).first()
        if subject:
            flash(f"Subject '{form.name.data}' already exists.", 'danger')
        else:
            subject = Subject(name=form.name.data, description=form.description.data, user=current_user)
            db.session.add(subject)
            db.session.commit()
            flash(f"Subject '{form.name.data}' has been added", 'success')
            return redirect(url_for('subjects.subjects_tasks'))
    elif request.method == 'GET':
        form.active.data = True
        
    return render_template('edit_subject.html', title='New Subject', form=form)

@subjects.route('/subject/<int:subject_id>')
def subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    return render_template('subject.html', title=subject.name, subject=subject)
    
@subjects.route('/subject/<int:subject_id>/update', methods=['GET', 'POST'])
@login_required
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        abort(403)
    form = SubjectForm()
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        subject.active = form.active.data
        db.session.commit()
        flash(f"Subject '{subject.name}' has been updated", 'success')
        return redirect(url_for('subjects.subject', subject_id=subject.id))
    elif request.method == 'GET':
        form.name.data = subject.name
        form.description.data = subject.description
        form.active.data = subject.active
    return render_template('edit_subject.html', title='Edit Subject', form=form)

@subjects.route('/subject/<int:subject_id>/delete', methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    if subject.user_id != current_user.id:
        abort(403)

    task = Task.query.filter_by(subject_id=subject_id).first()
    if task:
        flash(f"Task is found. Subject cannot be removed", 'danger')
        return
    timesheet = Timesheet.query.filter_by(subject_id=subject_id).first()
    if timesheet:
        flash(f"Timesheet is found. Subject cannot be removed", 'danger')
        return

    db.session.delete(subject)
    db.session.commit()
    flash(f"Subject '{subject.name}' has been removed", 'success')
    return redirect(url_for('subjects.subjects_tasks'))