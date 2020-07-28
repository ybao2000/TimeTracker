from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired
    
class TaskForm(FlaskForm):
    subject_id = HiddenField('Subject ID')
    subject_name = HiddenField('Subject Name')
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    active = BooleanField('Active')    
    submit = SubmitField('Submit')