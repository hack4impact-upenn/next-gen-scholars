from flask import url_for
import calendar
from datetime import datetime
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (StringField, IntegerField, SubmitField, SelectField, PasswordField)
from wtforms.validators import Email, EqualTo, InputRequired, Length
from wtforms.fields.html5 import EmailField

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


class AddTestScoreForm(Form):
	test_name = StringField(
		'Test Name', validators=[InputRequired(), Length(1, 100)])
	test_score = IntegerField(
		'Test Score', validators=[InputRequired()])
	test_month = StringField(
		'Test Month', validators=[InputRequired(), Length(1, 10)])
	test_year = StringField(
		'Test Year', validators=[InputRequired(), Length(1, 10)])
	submit = SubmitField('Add Test Score')

class AddRecommendationLetterForm(Form):
	name = StringField(
		'Name', validators=[InputRequired(), Length(1, 100)])
	category = StringField(
		'Position', validators=[InputRequired(), Length(1, 100)])
	status = StringField(
		'Status', validators=[InputRequired(), Length(1, 100)])
	submit = SubmitField('Add Recommendation Letter')

class AddEssayForm(Form):
	name = StringField(
		'Name', validators=[InputRequired(), Length(1, 100)])
	link = StringField(
		'Link', validators=[InputRequired(), Length(1, 100)])
	submit = SubmitField('Add Essay')
