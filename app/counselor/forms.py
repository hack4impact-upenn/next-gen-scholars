import itertools
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.widgets import TextArea
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import (PasswordField, StringField, SubmitField,
                            HiddenField, BooleanField, TextAreaField,
                            SelectField, IntegerField)
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length, Optional

from .. import db
from ..models import Role, User, TestName, College


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
    description = StringField(u'Description', widget=TextArea())
    # Input not required for either deadline.
    early_deadline = DateField(
        'Early Deadline (yyyy-mm-dd)',
        format='%Y-%m-%d',
        validators=[Optional()])
    regular_deadline = DateField(
        'Regular Deadline (yyyy-mm-dd)',
        format='%Y-%m-%d',
        validators=[Optional()])
    cost_of_attendance = IntegerField(
        'Cost of Attendance',
        validators=[InputRequired()])
    tuition = IntegerField(
        'Tuition',
        validators=[InputRequired()])
    room_and_board = IntegerField(
        'Room and Board',
        validators=[InputRequired()])
    image = StringField(
        'URL for image of college',
        validators=[InputRequired()]
    )
    submit = SubmitField('Add College Profile')


class EditCollegeProfileStep1Form(Form):
    name = QuerySelectField(
        'Select college you wish to edit',
        validators=[InputRequired()],
        get_label='name',
        query_factory=lambda: db.session.query(College).order_by('name'))
    submit = SubmitField('Continue')


class EditCollegeProfileStep2Form(Form):
    name = StringField(
        'College/University Name',
        validators=[InputRequired(), Length(1, 200)])
    description = StringField(u'Description', widget=TextArea())
    # Input not required for either deadline.
    early_deadline = DateField(
        'Early Deadline (yyyy-mm-dd)',
        format='%Y-%m-%d',
        validators=[Optional()])
    regular_deadline = DateField(
        'Regular Deadline (yyyy-mm-dd)',
        format='%Y-%m-%d',
        validators=[Optional()])
    cost_of_attendance = IntegerField(
        'Cost of Attendance',
        validators=[InputRequired()])
    tuition = IntegerField(
        'Tuition',
        validators=[InputRequired()])
    room_and_board = IntegerField(
        'Room and Board',
        validators=[InputRequired()])
    image = StringField(
        'URL to image of college',
        validators=[InputRequired()])
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
