from datetime import datetime, timedelta
from flask_login import current_user
from timetracker.models import Timesheet, Subject, Task
from timetracker import db

class TableCell:
    def __init__(self, date, workhours, description):
        self.Date = date
        self.Workhours = workhours
        self.Description = description

    def __repr__(self):
        return str(self.Workhours)

class TableRow:
    def __init__(self, subject, task, workhours):
        self.Subject = subject
        self.Task = task
        self.Workhours = workhours

def hasSubjectTask(dictTS, subject, task):
    for keys in dictTS.keys():
        if keys.Subject.id == subject.id:
            if task:
                if keys.Task and keys.Task.id == task.id:
                    return True
            elif not keys.Task:
                return True
    return False

def findTimesheet(tr, date, timesheets):
    for timesheet in timesheets:
        if timesheet.subject_id == tr.Subject.id and timesheet.date.date() == date:
            if timesheet.task_id:
                if tr.Task and timesheet.task_id == tr.Task.id:
                    return timesheet
            else:
                if not tr.Task:
                    return timesheet
    return None

def add_workhours(orig_workhours, workhours):
    if orig_workhours:
        return orig_workhours + workhours
    else:
        return workhours

def generate_dictTS(date=None):
    if date == None:
        date = datetime.now().date()
    start = date- timedelta(days=date.weekday()) # start of the week
    end = start + timedelta(days=6) # end of the week
    dates = []
    dictTS = {}
    sub_totals = [None, None, None, None, None, None, None]
    #generate dates
    dt = start
    while dt <= end:
        dates.append(dt)
        dt += timedelta(days=1)

    # generate rows
    timesheets = Timesheet.query.filter(Timesheet.user_id == current_user.id, db.func.date(Timesheet.date)>=start, db.func.date(Timesheet.date)<=end).all()
    if timesheets:
        for timesheet in timesheets:
            if not hasSubjectTask(dictTS, timesheet.subject, timesheet.task):
                dictTS[TableRow(timesheet.subject, timesheet.task, None)] = []
    subjects = Subject.query.filter(Subject.user_id==current_user.id, Subject.active==True).all()
    if subjects:
        for subject in subjects:
            if subject.tasks:
                for task in subject.tasks:
                    if task.active and not hasSubjectTask(dictTS, subject, task):
                        dictTS[TableRow(subject, task, None)] = []
            else:
                if not hasSubjectTask(dictTS, subject, None):
                    dictTS[TableRow(subject, None, None)] = []

    # generate cells for each row
    total = None
    for tr, cells in dictTS.items():
        i = 0
        for dt in dates:
            timesheet = findTimesheet(tr, dt, timesheets)
            if timesheet:
                cells.append(TableCell(dt, timesheet.workhours, timesheet.description))
                sub_totals[i] = add_workhours(sub_totals[i], timesheet.workhours)
                tr.Workhours = add_workhours(tr.Workhours, timesheet.workhours)
                total = add_workhours(total, timesheet.workhours)      
            else:
                cells.append(TableCell(dt, None, None))
            i += 1
    return dates, dictTS, sub_totals, total

def get_timesheet(subject_id, task_id, date):
    if task_id > 0:
        timesheet = Timesheet.query.filter(Timesheet.user_id==current_user.id, Timesheet.subject_id==subject_id, Timesheet.task_id==task_id, db.func.date(Timesheet.date)==date).first()
        return timesheet
    else:
        timesheet = Timesheet.query.filter(Timesheet.user_id==current_user.id, Timesheet.subject_id==subject_id, Timesheet.task_id==None, db.func.date(Timesheet.date)==date).first()
        return timesheet     