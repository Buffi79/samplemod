from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class ConfigForm(FlaskForm):
    level = StringField('loglevel', validators=[DataRequired()])
    format = StringField('format', validators=[DataRequired()])
    telsearchkey = StringField('telsearch', validators=[DataRequired()])
    submit = SubmitField('Save')
   # age = InterField('age', validators=[DataRequired()])

class EditentryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Save')
