from flask import render_template, Blueprint

subjects = Blueprint('subjects', __name__)

@subjects.route('/subjects_tasks')
def subjects_tasks():
    return render_template('subjects_tasks.html')  