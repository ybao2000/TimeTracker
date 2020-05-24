from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cdcd1a66-9d2d-11ea-bb37-0242ac130002'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetracker.db'
db = SQLAlchemy(app)

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

@app.route('/register')
def register():
	form = RegistrationForm()
	return render_template('register.html', form=form)  

@app.route('/subjects_tasks')
def subjects_tasks():
    return render_template('subjects_tasks.html')  

@app.route('/timesheets')
def timesheets():
    return render_template('timesheets.html')  