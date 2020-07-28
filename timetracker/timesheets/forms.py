import decimal
from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, TextAreaField, SubmitField, ValidationError, StringField
from wtforms.fields.html5 import DateField

class TimesheetForm(FlaskForm):
    subject_name = HiddenField("Subject")
    subject_id = HiddenField("Subject ID")
    task_name = HiddenField("Task")
    task_id = HiddenField("Task ID")
    date = HiddenField("Date")
    workhours = StringField("Work Hours")
    description = TextAreaField("Description")

    submit = SubmitField('Submit')

    def validate_workhours(self, workhours):
        if workhours.data:
            try:
                decimal.Decimal(workhours.data)
            except:
                raise ValidationError(f"invalid work hours")