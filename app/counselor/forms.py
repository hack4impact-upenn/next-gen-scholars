import itertools
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.widgets import TextArea
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (PasswordField, StringField, SubmitField,
                            HiddenField, BooleanField, TextAreaField,
                            SelectField, IntegerField, FloatField)
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional

from .. import db
from ..models import Role, User, TestName, College, Scholarship


class ChangeUserEmailForm(Form):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    submit = SubmitField('Update email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeAccountTypeForm(Form):
    role = QuerySelectField(
        'New account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    submit = SubmitField('Update role')


class InviteUserForm(Form):
    role = QuerySelectField(
        'Account type',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Role).order_by('permissions'))
    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    submit = SubmitField('Invite')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class NewUserForm(InviteUserForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    submit = SubmitField('Create')


class NewSMSAlertForm(Form):
    title = StringField(
        'Alert title', validators=[InputRequired(),
                                   Length(1, 64)])
    content = TextAreaField('Content', validators=[InputRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    time_choices = itertools.product(
        [12] + [x for x in range(1, 11)], ['00', '15', '30', '45'], repeat=1)
    time = SelectField(
        'Time',
        choices=[('{}:{}'.format(t[0], t[1]), '{}:{}'.format(t[0], t[1]))
                 for t in time_choices],
        validators=[InputRequired()])
    am_pm = SelectField(
        'AM/PM',
        choices=[('AM', 'AM'), ('PM', 'PM')],
        validators=[InputRequired()])
    submit = SubmitField('Add SMS Alert')


class EditSMSAlertForm(Form):
    title = StringField(
        'Alert title', validators=[InputRequired(),
                                   Length(1, 64)])
    content = TextAreaField('Content', validators=[InputRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    time_choices = itertools.product(
        [12] + [x for x in range(1, 11)], ['00', '15', '30', '45'], repeat=1)
    time = SelectField(
        'Time',
        choices=[('{}:{}'.format(t[0], t[1]), '{}:{}'.format(t[0], t[1]))
                 for t in time_choices],
        validators=[InputRequired()])
    am_pm = SelectField(
        'AM/PM',
        choices=[('AM', 'AM'), ('PM', 'PM')],
        validators=[InputRequired()])
    submit = SubmitField('Done Editing')


class AddChecklistItemForm(Form):
    item_text = StringField(
        'Checklist Item', validators=[InputRequired(),
                                      Length(1, 64)])
    date = DateField('Deadline', format='%Y-%m-%d', validators=[Optional()])
    assignee_ids = HiddenField('Assignee Ids')
    submit = SubmitField('Add checklist item')


class AddTestNameForm(Form):
    name = StringField(
        'Test Name', validators=[InputRequired(),
                                 Length(1, 150)])
    submit = SubmitField('Add Test Name')


class EditTestNameForm(Form):
    old_test = QuerySelectField(
        'Select test you wish to edit',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(TestName).order_by('name'))
    new_name = StringField(
        'New Test Name', validators=[InputRequired(),
                                     Length(1, 150)])
    submit = SubmitField('Edit Test Name')


class DeleteTestNameForm(Form):
    old_test = QuerySelectField(
        'Select test you wish to delete',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(TestName).order_by('name'))
    confirmation = BooleanField(
        'Are you sure you want to delete this test?',
        validators=[InputRequired()])
    submit = SubmitField('Delete Test Name')


class AddCollegeProfileForm(Form):
    name = StringField(
        'College/University Name',
        validators=[InputRequired(), Length(1, 200)])
    college_scorecard_url = StringField(
        'URL to the College Scorecard Profile or College Scorecard ID',
        validators=[Optional()])
    description = StringField(u'Description',
        validators=[Optional()], 
        widget=TextArea())
    early_deadline = DateField(
        'Early Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    regular_deadline = DateField(
        'Regular Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    scholarship_deadline = DateField(
        'Scholarship Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    fafsa_deadline = DateField(
        'FAFSA Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    acceptance_deadline = DateField(
        'Acceptance Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    image = StringField(
        'URL for image of college',
        validators=[Optional()]
    )
    submit = SubmitField('Add College Profile')


class EditCollegeProfileStep1Form(Form):
    name = QuerySelectField(
        'Select college you wish to edit',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(College).order_by('name'))
    submit = SubmitField('Continue')


class AddResourceForm(Form):
    resource_url = StringField(
        u'Link to Resource',
        validators=[InputRequired()]
    )
    title = StringField(
        u'Resource Title',
        validators=[InputRequired()]
    )
    description = StringField(
        u'Resource Description', 
        validators=[InputRequired()],
        widget=TextArea()
    )
    image_url = StringField(
        u'URL of Resource Image',
        validators=[InputRequired()]
    )
    submit = SubmitField('Add Resource')


class EditResourceForm(Form):
    resource_url = StringField(
        u'Link to Resource',
        validators=[InputRequired()]
    )
    title = StringField(
        u'Resource Title',
        validators=[InputRequired()]
    )
    description = StringField(
        u'Resource Description', 
        validators=[InputRequired()],
        widget=TextArea()
    )
    image_url = StringField(
        u'URL of Resource Image',
        validators=[InputRequired()]
    )
    submit = SubmitField('Edit Resource')


class EditCollegeProfileStep2Form(Form):
    name = StringField(
        'College/University Name',
        validators=[InputRequired(), Length(1, 200)])
   
    college_scorecard_url = StringField(
        'URL to the College Scorecard Profile or College Scorecard ID',
        validators=[Optional()])
    # Input not required for either deadline.
    description = StringField(
        u'Description', 
        widget=TextArea(),
        validators=[Optional()])
    early_deadline = DateField(
        'Early Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    regular_deadline = DateField(
        'Regular Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    scholarship_deadline = DateField(
        'Scholarship Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    fafsa_deadline = DateField(
        'Fafsa Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    acceptance_deadline = DateField(
        'Acceptance Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    image = StringField(
        'URL to image of college',
        validators=[Optional()])
    submit = SubmitField('Save College Profile')


class DeleteCollegeProfileForm(Form):
    name = QuerySelectField(
        'Select college you wish to delete',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(College).order_by('name'))
    confirmation = BooleanField(
        'Are you sure you want to delete this college?',
        validators=[InputRequired()])
    submit = SubmitField('Delete College Profile')


class ParseAwardLetterForm(Form):
    cost = FloatField('Cost', validators=[InputRequired()])
    loans = FloatField('Loans', validators=[InputRequired()])
    work_study = FloatField('Work Study', validators=[InputRequired()])
    financial_aid = FloatField('Financial Aid', validators=[InputRequired()])
    institutional_scholarships = FloatField('Institutional Scholarships', validators=[InputRequired()])
    net_cost = FloatField('Net Cost to Student', validators=[InputRequired()])
    submit = SubmitField('Parse Award Letter')

class AddScholarshipProfileForm(Form):
    name = StringField(
        'Scholarship Name',
        validators=[InputRequired()])
    description = StringField(u'Description', widget=TextArea())
    # Input not required for either deadline.
    deadline = DateField(
        'Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    award_amount = FloatField('Award Amount', validators=[InputRequired()])
    category = StringField('Category of Scholarship (If none, put General)', validators=[Optional()])
    merit_based = BooleanField('Merit Based')
    service_based = BooleanField('Service Based')
    need_based = BooleanField('Need Based')
    interview_required = BooleanField('Interview Required')
    minimum_gpa = FloatField('Minimum GPA', validators=[Optional()])
    link = StringField('Link to more information', validators=[Optional()])
    submit = SubmitField('Add Scholarship Profile')


class EditScholarshipProfileStep1Form(Form):
    name = QuerySelectField(
        'Select scholarship you wish to edit',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Scholarship).order_by('name'))
    submit = SubmitField('Continue')


class EditScholarshipProfileStep2Form(Form):
    name = StringField(
        'College/University Name',
        validators=[InputRequired(), Length(1, 200)])
    description = StringField(u'Description', widget=TextArea())
    # Input not required for either deadline.
    deadline = DateField(
        'Deadline (mm-dd-yyyy)',
        format='%Y-%m-%d',
        validators=[Optional()])
    award_amount = FloatField('Award Amount', validators=[InputRequired()])
    category = StringField('Category of Scholarship (If none, put General)', validators=[Optional()])
    merit_based = BooleanField('Merit Based')
    service_based = BooleanField('Service Based')
    need_based = BooleanField('Need Based')
    interview_required = BooleanField('Interview Required')
    minimum_gpa = FloatField('Minimum GPA', validators=[Optional()])
    link = StringField('Link to more information', validators=[Optional()])
    submit = SubmitField('Update Scholarship Profile')


class DeleteScholarshipProfileForm(Form):
    name = QuerySelectField(
        'Select scholarship you wish to delete',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(Scholarship).order_by('name'))
    confirmation = BooleanField(
        'Are you sure you want to delete this scholarship?',
        validators=[InputRequired()])
    submit = SubmitField('Delete Scholarship Profile')
