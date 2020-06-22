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
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional, NumberRange
from wtforms.fields.html5 import EmailField
import re

from .. import db
from ..models import TestName, College, TestScore


class EditCommonAppEssayForm(Form):
    link = StringField(
        'Link to Common App Essay',
        validators=[InputRequired(), Length(1, 100)])
    status = SelectField(
        'Status',
        choices=[('Incomplete', 'Incomplete'), ('Waiting', 'Waiting'),
                 ('Reviewed', 'Reviewed'), ('Edited', 'Edited'), ('Done',
                                                                  'Done')], 
        #default=('Waiting', 'Waiting'),                                                     
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
                                  Length(1, 100)])
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
    for i in range(11):
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

    # must override validate method in order to cross-check scores across different fields
    def validate(self):
        
        # first run the normal non-overriden validate method
        if not Form.validate(self):
            return False
        
        # see if there's existing score in database with same test type, month, and year 
        test_name = self.data.get('test_name').name
        test_month = self.data.get('month')
        test_year = self.data.get('year')

        test = db.session.query(TestScore).filter_by(name=test_name, month=test_month, year=test_year).first()
        if test is not None:
            self.test_name.errors.append('Please enter a different date for this test or edit the existing score.')
            return False
        
        # TODO: Read me from a database or something... let admin be able to edit valid test score ranges
        valid_ranges = \
            {'ACT' : (0,36) ,
            'SAT' : (0,1600),
            'SAT Subject Test - Math Level 2' : (0,800),
            'AP Physics 1' : (0,5),
            'AP Chemistry' : (0, 5),
            'AP Computer Science A' : (0, 5),
            'SAT Subject Test - Math Level 1' : (0, 800),
            'AP Physics 2' : (0, 5),
            'AP English Language & Composition': (0, 5),
            'SAT Subject Test - Chemistry' : (0, 800),
            'SAT Subject Test - Physics' : (0, 800)
            }
        
        valid_range = valid_ranges.get(test_name, -1)

        # checking to see if the test name shows up in database; 
        # this error should not happen under normal circumstances
        if valid_range == -1:
            self.test_name.errors.append('Not a valid test.') 
            return False

        # check to see if range is valid
        if not (self.data.get('score') >= valid_range[0] and self.data.get('score') <= valid_range[1]):
            self.score.errors.append("The " + test_name + '\'s score must be between ' + str(valid_range[0]) +' and ' + \
                    str(valid_range[1])) 

            # TODO: check to see if score is valid score in increments of x (i.e. SAT score must be in increments of 10)
            return False 

        return True

class EditValidTestScoreRanges(Form):
    #TODO: implement me
    test_name = QuerySelectField(
        'Test Name',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(TestName).order_by('name'))
    min_num = IntegerField('Minimum Valid Test Score', validators=[InputRequired()])
    max_num = IntegerField('Maximum Valid Test Score', validators=[InputRequired()])


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
    phone_number = StringField(
        'Phone number', validators=[InputRequired()])
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
    
    def strip_all(self):
        raise ValidationError(self.data)

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

    
    def validate_award_amount(form, field):
        award_amount = str(field.data)

        # regex makes sure that vals either have no decimal, a decimal and a tenths places, a decimal 
        # and a hundreths place
        if re.match('^\d+(\.\d(\d)?)?$', award_amount) is None:
            raise ValidationError('Monetary amount must be in the format: xx, xx.xx or xx.xx')


class EditStudentScholarshipForm(Form):
    name = StringField('Scholarship Name', validators=[InputRequired()])
    award_amount = FloatField('Award Amount', validators=[InputRequired()])
    submit = SubmitField('Update Scholarship Award')

    def validate_award_amount(form, field):
        award_amount = str(field.data)
        if re.match('^\d+(\.\d(\d)?)?$', award_amount) is None:
            raise ValidationError('Monetary amount must be in the format: xx, xx.xx or xx.xx')