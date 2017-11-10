from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (PasswordField, StringField, SubmitField,
                            IntegerField, FloatField, SelectField, BooleanField)
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

class EditStudentProfile(Form):
    grade = SelectField(
        'Grade', choices=[('9', '9th Grade'),
                          ('10', '10th Grade'),
                          ('11', '11th Grade'),
                          ('12', '12th Grade')])
    high_school = StringField(
        'High School', validators=[InputRequired(), Length(1, 100)])
    graduation_year = IntegerField(
        'Graduation Year', validators=[InputRequired()])
    gpa = FloatField(
        'GPA', validators=[InputRequired()])
    fafsa_status = SelectField(
        'FAFSA Status', choices=[('Incomplete', 'Incomplete'),
                                 ('Complete', 'Complete'),
                                 ('In Progress', 'In Progress')])
    district = StringField(
        'District', validators=[InputRequired(), Length(1, 100)])
    city = StringField(
        'City', validators=[InputRequired(), Length(1, 100)])
    state = StringField(
        'State', validators=[InputRequired(), Length(1, 100)])
    early_deadline = BooleanField('I Have An Early Deadline')
    submit = SubmitField('Update Profile')

class AddCollegeForm(Form):
    name = StringField(
        'College Name', validators=[InputRequired(), Length(1, 100)])
    submit = SubmitField('Add College')

class AddMajorForm(Form):
    major = StringField(
        'Major', validators=[InputRequired(), Length(1, 100)])
    submit = SubmitField('Add Major')
