from flask import url_for
import calendar
from datetime import datetime
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (PasswordField, StringField, SubmitField,
                            IntegerField, FloatField, SelectField,
                            BooleanField)
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional
from wtforms.fields.html5 import EmailField

from .. import db
from ..models import TestName, College


class EditCommonAppEssayForm(Form):
    link = StringField(
        'Link to Common App Essay',
        validators=[InputRequired(), Length(1, 64)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Waiting', 'Waiting'),
                 ('Reviewed', 'Reviewed'), ('Edited', 'Edited'), ('Done',
                                                                  'Done')],
        validators=[InputRequired()])
    submit = SubmitField('Update essay link')


class EditCollegeForm(Form):
    college_name = StringField(
        'College Name', validators=[InputRequired(),
                                    Length(1, 64)])
    submit = SubmitField('Update college name')


class EditTestScoreForm(Form):
    month_choices = []
    for i in range(1, 13):
        month_choices.append((calendar.month_name[i], calendar.month_name[i]))
    year_choices = []
    today = datetime.today()
    for i in range(0, 8):
        year_choices.append((str(today.year - 8 + i), str(today.year - 8 + i)))
    test_name = QuerySelectField(
        'Test Name',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(TestName).order_by('name'))
    month = SelectField(
        u'Month', choices=month_choices, validators=[InputRequired()])
    year = SelectField(
        u'Year', choices=year_choices, validators=[InputRequired()])
    score = IntegerField('Test Score', validators=[InputRequired()])
    submit = SubmitField('Update test score')


class EditSupplementalEssayForm(Form):
    essay_name = StringField(
        'Essay Name', validators=[InputRequired(),
                                  Length(1, 64)])
    link = StringField(
        'Essay Link', validators=[InputRequired(),
                                  Length(1, 64)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Waiting', 'Waiting'),
                 ('Reviewed', 'Reviewed'), ('Edited', 'Edited'), ('Done',
                                                                  'Done')],
        validators=[InputRequired()])
    submit = SubmitField('Update essay')


class AddChecklistItemForm(Form):
    item_text = StringField(
        'Checklist Item', validators=[InputRequired(),
                                      Length(1, 64)])
    date = DateField('Deadline', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Add checklist item')


class EditChecklistItemForm(Form):
    item_text = StringField(
        'New text', validators=[InputRequired(),
                                Length(1, 64)])
    date = DateField('Deadline', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Update checklist item')


class AddTestScoreForm(Form):
    month_choices = []
    for i in range(1, 13):
        month_choices.append((calendar.month_name[i], calendar.month_name[i]))
    year_choices = []
    today = datetime.today()
    for i in range(8):
        year_choices.append((str(today.year - i), str(today.year - i)))
    test_name = QuerySelectField(
        'Test Name',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(TestName).order_by('name'))
    month = SelectField(
        u'Month', choices=month_choices, validators=[InputRequired()])
    year = SelectField(
        u'Year', choices=year_choices, validators=[InputRequired()])
    score = IntegerField('Test Score', validators=[InputRequired()])
    submit = SubmitField('Add test score')


class AddRecommendationLetterForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 100)])
    category = StringField(
        'Position', validators=[InputRequired(),
                                Length(1, 100)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Submitted', 'Submitted'),
                 ('Pending', 'Pending')])
    submit = SubmitField('Add Recommendation Letter')


class EditRecommendationLetterForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 100)])
    category = StringField(
        'Position', validators=[InputRequired(),
                                Length(1, 100)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Submitted', 'Submitted'),
                 ('Pending', 'Pending')],
        validators=[InputRequired()])
    submit = SubmitField('Update Recommendation Letter')


class AddSupplementalEssayForm(Form):
    name = StringField('Name', validators=[InputRequired(), Length(1, 100)])
    link = StringField('Link', validators=[InputRequired(), Length(1, 100)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Waiting', 'Waiting'),
                 ('Reviewed', 'Reviewed'), ('Edited', 'Edited'), ('Done',
                                                                  'Done')],
        validators=[InputRequired()])
    submit = SubmitField('Add Supplemental Essay')


class AddCommonAppEssayForm(Form):
    link = StringField('Link', validators=[InputRequired(), Length(1, 100)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Submitted', 'Submitted'),
                 ('Pending', 'Pending')],
        validators=[InputRequired()])
    submit = SubmitField('Add Common App Essay')


class EditStudentProfile(Form):
    grade = SelectField(
        'Grade',
        choices=[('9', '9th Grade'), ('10', '10th Grade'),
                 ('11', '11th Grade'), ('12', '12th Grade')])
    high_school = StringField(
        'High School', validators=[InputRequired(),
                                   Length(1, 100)])
    graduation_year = IntegerField(
        'Graduation Year', validators=[InputRequired()])
    unweighted_gpa = FloatField('Unweighted GPA', validators=[InputRequired()])
    weighted_gpa = FloatField('Weighted GPA', validators=[Optional()])
    fafsa_status = SelectField(
        'FAFSA Status',
        choices=[('Incomplete', 'Incomplete'), ('Submitted', 'Submitted'),
                 ('In Progress', 'In Progress')])
    early_deadline = SelectField(
        'Have Early Deadline', choices=[('True', 'Yes'), ('False', 'No')])
    district = StringField(
        'District', validators=[InputRequired(),
                                Length(1, 100)])
    city = StringField('City', validators=[InputRequired(), Length(1, 100)])
    state = StringField('State', validators=[InputRequired(), Length(1, 100)])
    submit = SubmitField('Update Profile')


class AddCollegeForm(Form):
    name = QuerySelectField(
        'College Name',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(College).order_by('name'))
    lvl = SelectField(
        'Interest Level',
        choices= [('High','High'), ('Medium','Medium'),
        ('Low','Low')],
        validators=[InputRequired()])
    submit = SubmitField('Add College')


class AddMajorForm(Form):
    major = StringField('Major', validators=[InputRequired(), Length(1, 100)])
    submit = SubmitField('Add Major')


class AddAcceptanceForm(Form):
    link = StringField('Award Letter Link', validators=[InputRequired(), Length(1, 100)])
    college = QuerySelectField(
        'College Name',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(College).order_by('name'))
    status = SelectField(
        'Status',
        choices=[('Accepted', 'Accepted'),('Accepted with award letter',
                  'Accepted with award letter'), ('Pending Award Letter Parsing',
                   'Pending Award Letter Parsing')],
        validators=[InputRequired()])
    submit = SubmitField('Add Acceptance')


class EditAcceptanceForm(Form):
    link = StringField(
        'Award Letter Link', validators=[InputRequired(),
                                         Length(1, 100)])
    college = QuerySelectField(
        'College Name',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(College).order_by('name'))
    status = SelectField(
        'Status',
        choices=[('Accepted', 'Accepted'),
                 ('Accepted with award letter',
                  'Accepted with award letter'), ('Pending Award Letter Parsing', 
                  'Pending Award Letter Parsing')],
        validators=[InputRequired()])
    submit = SubmitField('Update Acceptance')


class AddStudentScholarshipForm(Form):
    name = StringField('Scholarship Name', validators=[InputRequired()])
    award_amount = FloatField('Award Amount', validators=[InputRequired()])
    submit = SubmitField('Add Scholarship Award')

class EditStudentScholarshipForm(Form):
    name = StringField('Scholarship Name', validators=[InputRequired()])
    award_amount = FloatField('Award Amount', validators=[InputRequired()])
    submit = SubmitField('Update Scholarship Award')