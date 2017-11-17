from flask_wtf import Form
from wtforms import ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import PasswordField, StringField, SubmitField, HiddenField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .. import db
from ..models import Role, User, TestName


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


class AddChecklistItemForm(Form):
    item_text = StringField(
        'Checklist Item', validators=[InputRequired(),
                                      Length(1, 64)])
    date = DateField(
        'Deadline', format='%Y-%m-%d', validators=[InputRequired()])
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

