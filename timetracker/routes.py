from flask import render_template, request, url_for
from timetracker.forms import RegistrationForm
from timetracker import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			return render_template('login.html')

	return render_template('register.html', form=form)  

@app.route('/subjects_tasks')
def subjects_tasks():
    return render_template('subjects_tasks.html')  

@app.route('/timesheets')
def timesheets():
    return render_template('timesheets.html')  