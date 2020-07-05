from flask import render_template, request, url_for, flash, redirect, abort, Blueprint
from timetracker.todos.forms import TodoForm
from timetracker import db
from timetracker.models import Todo
from flask_login import login_required, current_user
from sqlalchemy import desc
from datetime import datetime

todos = Blueprint('todos', __name__)

@todos.route('/todos')
@login_required
def todo_list():
	todos = Todo.query.filter_by(user_id=current_user.id).order_by(desc(Todo.date_created)).all()
	return render_template('todos.html', todos=todos)

@todos.route('/todos/new', methods=['GET', 'POST'])
@login_required
def new_todo():
	form = TodoForm()
	if form.validate_on_submit():  # POST only
		todo = Todo(title=form.title.data, description=form.description.data, user_id=current_user.id)
		db.session.add(todo)
		db.session.commit()
		flash(f"Todo '{form.title.data}' has beed added'", category="success")
		return redirect(url_for('todos.todo_list'))

	elif request.method == 'GET':  # GET only
		return render_template('edit_todo.html', title='New Todo', form=form)

@todos.route('/todos/<int:todo_id>')
@login_required
def todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)

	return render_template('todo.html', title='Todo', todo=todo)

@todos.route('/todos/<int:todo_id>/update', methods=['GET', 'POST'])
@login_required
def update_todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)
	if todo.user_id != current_user.id:
		abort(403)

	form = TodoForm()
	if form.validate_on_submit():  # POST only
		todo.title = form.title.data
		todo.description = form.description.data
		db.session.commit()
		flash(f"Todo '{form.title.data}' has beed updated'", category="success")
		return redirect(url_for('todos.todo_list'))

	elif request.method == 'GET':  # GET only
		form.title.data = todo.title
		form.description.data = todo.description

		return render_template('edit_todo.html', title='Update Todo', form=form)

@todos.route('/todos/<int:todo_id>/complete', methods=['POST'])
@login_required
def complete_todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)
	if todo.user_id != current_user.id:
		abort(403)

	todo.date_completed = datetime.now()
	db.session.commit()
	flash(f"Todo '{todo.title}' has beed completed'", category="success")
	return redirect(url_for('todos.todo_list'))	

@todos.route('/todos/<int:todo_id>/delete', methods=['POST'])
@login_required
def delete_todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)
	if todo.user_id != current_user.id:
		abort(403)

	db.session.delete(todo)
	db.session.commit()
	flash(f"Todo '{todo.title}' has beed deleted'", category="success")
	return redirect(url_for('todos.todo_list'))			
