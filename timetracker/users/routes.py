from flask import render_template, request, url_for, flash, redirect, abort, Blueprint
from timetracker.users.forms import RegistrationForm, LoginForm
from timetracker import db, bcrypt
from timetracker.models import User
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from datetime import datetime

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			# return render_template("home")
			return redirect(url_for('general.home'))
		else:
			flash("Login failed. please check email and password", category="danger")

	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('general.home'))

@users.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=pw_hash)
		db.session.add(user)
		db.session.commit()
		
		# return render_template('login.html')
		return redirect(url_for('users.login'))
		
	return render_template('register.html', title='Registration', form=form)  

@users.route('/profile')
@login_required
def profile():
	return render_template('profile.html')
