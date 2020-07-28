from datetime import datetime, timedelta
from calendar import monthrange

from io import StringIO, BytesIO
from xlsxwriter import Workbook
import mimetypes
import decimal
from flask import render_template, request, redirect, Blueprint, flash, url_for, send_file, Response
from flask_login import login_required, current_user
from timetracker import db
from timetracker.timesheets.forms import TimesheetForm
from timetracker.timesheets.tableHelper import generate_dictTS, get_timesheet, add_workhours
from timetracker.timesheets.excelHelper import set_column_autowidth, week_of_month
from timetracker.models import Subject, Task, Timesheet

timesheets = Blueprint('timesheets', __name__)

@timesheets.route('/weekly_timesheets')
@login_required
def weekly_timesheets():
    date = request.args.get('date')
    if date:
        dt = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        dt = datetime.now().date()
    dates, dictTS, sub_totals, total = generate_dictTS(dt)
    return render_template('weekly_timesheets.html', title='Weekly Timesheets', date=dt, dates=dates, dictTS=dictTS, sub_totals=sub_totals, total=total)

@timesheets.route('/timesheet', methods=['GET', 'POST'])
@login_required
def timesheet():
    form = TimesheetForm()
    if form.validate_on_submit():
        subjectId = int(form.subject_id.data)
        taskId = -1
        if form.task_id.data:
            taskId = int(form.task_id.data)
        dt = datetime.strptime(form.date.data, "%Y-%m-%d").date()
        timesheet = get_timesheet(subjectId, taskId, dt)
        if timesheet:   #timesheet exists
            if form.workhours.data: # workhours exists
                timesheet.workhours = decimal.Decimal(form.workhours.data)
                timesheet.descrioption = form.description.data
                db.session.commit()
                flash(f"timesheet has been updated", 'success')
            else:
                db.session.delete(timesheet)
                db.session.commit()
                flash(f"timesheet has been removed", 'success')

        else:
            if form.workhours.data: #workhours exists
                    workhours = decimal.Decimal(form.workhours.data)
                    timesheet = Timesheet(user_id=current_user.id, subject_id=subjectId, task_id=taskId if taskId >0 else None, date=dt, workhours=workhours, description=form.description.data)
                    db.session.add(timesheet)
                    db.session.commit()
                    flash(f"timesheet has been added", 'success')
            else:
                    flash(f"please enter work hours", 'danger')
                    return
        return redirect(url_for('timesheets.weekly_timesheets', date=dt))

    elif request.method == 'GET':
        subject_id = request.args.get('subject_id')
        subjectId = int(subject_id)
        form.subject_id.data = subjectId
        subject = Subject.query.get(subjectId)
        form.subject_name.data = subject.name

        task_id = request.args.get('task_id')
        if task_id:
            taskId = int(task_id)
            form.task_id.data = taskId
            if taskId > 0:
                task = Task.query.get(taskId)
                form.task_name.data = task.name
        date = request.args.get('date')
        dt =datetime.strptime(date, "%Y-%m-%d").date()
        form.date.data = dt

        timesheet = get_timesheet(subjectId, taskId if task_id else -1, dt)
        if timesheet:
            form.workhours.data = timesheet.workhours
            form.description.data = timesheet.description
        
    return render_template('edit_timesheet.html', title='Timesheet', form=form)

@timesheets.route('/weekly_report')
@login_required
def weekly_report():
    date = request.args.get('date')
    if date:
        dt = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        dt = datetime.now().date()
    start = dt- timedelta(days=dt.weekday()) # start of the week
    end = start + timedelta(days=6) # end of the week            
    timesheets = Timesheet.query.filter(Timesheet.user_id == current_user.id, db.func.date(Timesheet.date)>=start, db.func.date(Timesheet.date)<=end).order_by(Timesheet.date).all()

    output = BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('weekly timesheet')
    row = 1
    total = 0
    bold = workbook.add_format({'bold': True})
    for timesheet in timesheets:
        worksheet.write(row, 0, datetime.strftime(timesheet.date, "%m/%d/%Y"))
        subject_task = timesheet.subject.name
        if timesheet.task:
            subject_task += f", {timesheet.task.name}"
        worksheet.write(row, 1, subject_task)
        worksheet.write(row, 2, timesheet.workhours)
        worksheet.write(row, 3, timesheet.description)
        total = add_workhours(total, timesheet.workhours)
        row += 1
    worksheet.write(0, 0, "Sum", bold)
    worksheet.write(0, 2, total, bold)

    for i in range(4):
        set_column_autowidth(worksheet, i)
    workbook.close()
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":f"attachment;filename=weekly_report_{current_user.username}_{date}.xlsx"})

@timesheets.route('/monthly_report')
@login_required
def monthly_report():
    date = request.args.get('date')
    if date:
        dt = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        dt = datetime.now().date()
    start = dt.replace(day=1) # start of the month
    end = start + timedelta(days=monthrange(dt.year, dt.month)[1]-1)
    timesheets = Timesheet.query.filter(Timesheet.user_id == current_user.id, db.func.date(Timesheet.date)>=start, db.func.date(Timesheet.date)<=end).order_by(Timesheet.date).all()

    weeks = []
    weekList = []
    hour = 0
    prev_week_num = 0
    for timesheet in timesheets:
        week_num = week_of_month(timesheet.date)
        if week_num > prev_week_num:
            if weekList:
                weeks.append((prev_week_num, hour, weekList))         
                weekList = []
                hour = 0
            prev_week_num = week_num
            
        weekList.append(timesheet)
        hour = add_workhours(hour, timesheet.workhours)

    if weekList:
        weeks.append((prev_week_num, hour, weekList))

    output = BytesIO()
    workbook = Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('monthly timesheet')
    bold = workbook.add_format()
    bold.set_bold(True)
    center = workbook.add_format()
    center.set_align('center')
    center_bold = workbook.add_format()
    center_bold.set_bold(True)
    center_bold.set_align('center')
    row = 0
    worksheet.write(0, 0, "Date", bold)
    worksheet.write(0, 1, "Project, Task", bold)
    worksheet.write(0, 2, "Time Spent (Hour)", center_bold)
    # worksheet.write(0, 3, "Description", bold)

    row += 1
    for week in weeks:
        for timesheet in week[2]:
            worksheet.write(row, 0, datetime.strftime(timesheet.date, "%m/%d/%Y"))
            subject_task = timesheet.subject.name
            if timesheet.task:
                subject_task += f", {timesheet.task.name}"
            worksheet.write(row, 1, subject_task)
            worksheet.write(row, 2, timesheet.workhours, center)
            worksheet.write(row, 3, timesheet.description)
            row += 1
        row += 1
        worksheet.write(row, 0, "Sum", bold)
        worksheet.write(row, 2, week[1], center_bold)
        worksheet.write(row, 3, f"Week {week[0]}", bold)
        row += 1

    for i in range(4):
        set_column_autowidth(worksheet, i)
    workbook.close()
    output.seek(0)
    return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":f"attachment;filename=monthly_report_{current_user.username}_{date}.xlsx"})
