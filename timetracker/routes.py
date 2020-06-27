from flask import render_template, request, url_for, flash, redirect, abort
from timetracker.forms import RegistrationForm, LoginForm, TodoForm
from timetracker import app, db, bcrypt
from timetracker.models import User, Todo
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			# return render_template("home")
			return redirect(url_for('home'))
		else:
			flash("Login failed. please check email and password", category="danger")

	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=pw_hash)
		db.session.add(user)
		db.session.commit()
		
		# return render_template('login.html')
		return redirect(url_for('login'))
		
	return render_template('register.html', title='Registration', form=form)  

@app.route('/profile')
@login_required
def profile():
	return render_template('profile.html')

@app.route('/todos')
@login_required
def todos():
	todos = Todo.query.filter_by(user_id=current_user.id).order_by(desc(Todo.date_created)).all()
	return render_template('todos.html', todos=todos)

@app.route('/subjects_tasks')
def subjects_tasks():
    return render_template('subjects_tasks.html')  

@app.route('/timesheets')
def timesheets():
    return render_template('timesheets.html')  

@app.route('/todos/new', methods=['GET', 'POST'])
@login_required
def new_todo():
	form = TodoForm()
	if form.validate_on_submit():  # POST only
		todo = Todo(title=form.title.data, description=form.description.data, user_id=current_user.id)
		db.session.add(todo)
		db.session.commit()
		flash(f"Todo '{form.title.data}' has beed added'", category="success")
		return redirect(url_for('todos'))

	elif request.method == 'GET':  # GET only
		return render_template('edit_todo.html', title='New Todo', form=form)

@app.route('/todos/<int:todo_id>')
@login_required
def todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)

	return render_template('todo.html', title='Todo', todo=todo)

@app.route('/todos/<int:todo_id>/update', methods=['GET', 'POST'])
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
		return redirect(url_for('todos'))

	elif request.method == 'GET':  # GET only
		form.title.data = todo.title
		form.description.data = todo.description

		return render_template('edit_todo.html', title='Update Todo', form=form)

	