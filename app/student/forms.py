from flask import url_for
import calendar
from datetime import datetime
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (StringField, IntegerField, SubmitField, SelectField)
from wtforms.validators import Email, EqualTo, InputRequired, Length

class EditCommonAppEssayForm(Form):
    link = StringField(
        'Link to Common App Essay', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update essay link')

class EditCollegeForm(Form):
    college_name = StringField(
        'College Name', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update college name')

class EditTestScoreForm(Form):
    month_choices = []
    for i in range(1, 13):
        month_choices.append((calendar.month_name[i], calendar.month_name[i]))
    year_choices = []
    today = datetime.today()
    for i in range(0, 8):
        year_choices.append((str(today.year - 8 + i), str(today.year - 8 + i)))
    test_name = StringField(
        'Test Name', validators=[InputRequired()])
    month = SelectField(u'Month', choices=month_choices, validators=[InputRequired()])
    year = SelectField(u'Year', choices=year_choices, validators=[InputRequired()])
    score = IntegerField(
        'Test Score', validators=[InputRequired()])
    submit = SubmitField('Update test score')

class EditSupplementalEssayForm(Form):
    essay_name = StringField(
        'Essay Name', validators=[InputRequired(), Length(1, 64)])
    link = StringField(
        'Essay Link', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update essay')

class AddChecklistItemForm(Form):
    item_text = StringField(
        'Checklist Item', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Add checklist item')

class EditChecklistItemForm(Form):
    item_text = StringField(
        'New text', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update checklist item')