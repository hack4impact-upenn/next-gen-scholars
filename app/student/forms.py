from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .. import db
from ..models import Role, User


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
