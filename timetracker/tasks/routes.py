from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from timetracker import db
from timetracker.models import Subject, Task, Timesheet
from timetracker.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)

@tasks.route('/subjects/<int:subject_id>/newtask', methods=['GET', 'POST'])
@login_required
def new_task(subject_id):
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data, description=form.description.data, subject_id=subject_id)
        db.session.add(task)
        db.session.commit()
        flash(f"Task '{form.name.data}' has been added to Subject '{form.subject_name.data}'", 'success')
        return redirect(url_for('subjects.subject', subject_id=subject_id))
    elif request.method == 'GET':
        subject = Subject.query.get(subject_id)
        if subject:
            form.subject_id.data = subject.id
            form.subject_name.data = subject.name
            form.active.data = True
        else:
            flash(f"Subject not found!")
            return redirect(url_for('general.home'))

    return render_template('edit_task.html', title='New Task', form=form)

@tasks.route('/task/<int:task_id>')
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.name, task=task)

@tasks.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.subject.user_id != current_user.id:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        task.active = form.active.data
        db.session.commit()
        flash(f"Task '{task.name}' has been updated", 'success')
        return redirect(url_for('subjects.subject', subject_id=task.subject.id))
    elif request.method == 'GET':
        form.subject_id.data = task.subject.id
        form.subject_name.data = task.subject.name
        form.name.data = task.name
        form.description.data = task.description
        form.active.data = task.active
    return render_template('edit_task.html', title='Update Task', form=form)

@tasks.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.subject.user_id != current_user.id:
        abort(403)

    timesheet = Timesheet.query.filter_by(task_id=task_id).first()
    if timesheet:
        flash(f"Timesheet is found. Task cannot be removed", 'danger')
        return

    db.session.delete(task)
    db.session.commit()
    flash(f"Task '{task.name}' has been removed", 'success')
    return redirect(url_for('subjects.subject', subject_id=task.subject.id))

