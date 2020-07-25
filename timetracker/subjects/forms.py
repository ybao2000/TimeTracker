from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired

class SubjectForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  description = TextAreaField('Description')
  active = BooleanField("Active")
  submit = SubmitField('Submit')