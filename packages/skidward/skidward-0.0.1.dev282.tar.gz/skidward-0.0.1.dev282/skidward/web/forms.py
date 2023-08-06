from wtforms import StringField, validators
from flask_wtf import FlaskForm


class TaskContextForm(FlaskForm):
    key = StringField("Key", [validators.DataRequired()])
    value = StringField("Value", [validators.DataRequired()])
