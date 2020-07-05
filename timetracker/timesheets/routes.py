from flask import render_template, Blueprint

timesheets = Blueprint('timesheets', __name__)

@timesheets.route('/timesheets')
def timesheet_list():
    return render_template('timesheets.html')  