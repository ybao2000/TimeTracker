from flask import Flask, render_template
app = Flask(__name__)

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
    return render_template('register.html')  

@app.route('/subjects_tasks')
def subjects_tasks():
    return render_template('subjects_tasks.html')  

@app.route('/timesheets')
def timesheets():
    return render_template('timesheets.html')  