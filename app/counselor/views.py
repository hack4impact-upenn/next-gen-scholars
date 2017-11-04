from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask_rq import get_queue

from .forms import (ChangeAccountTypeForm, ChangeUserEmailForm, InviteUserForm,
                    NewUserForm, AddChecklistItemForm)
from . import counselor
from .. import db
from ..decorators import counselor_required
from ..decorators import admin_required
from ..email import send_email
from ..models import Role, User, StudentProfile, EditableHTML, ChecklistItem

@counselor.route('/')
@login_required
@counselor_required
def index():
    """Counselor dashboard page."""
    return render_template('counselor/index.html')


@counselor.route('/new-user', methods=['GET', 'POST'])
@login_required
@counselor_required
def new_user():
    """Create a new user."""
    form = NewUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User {} successfully created'.format(user.full_name()),
              'form-success')
    return render_template('counselor/new_user.html', form=form)

@counselor.route('/invite-user', methods=['GET', 'POST'])
@login_required
@counselor_required
def invite_user():
    """Invites a new user to create an account and set their own password."""
    form = InviteUserForm()
    if form.validate_on_submit():
        user = User(
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        invite_link = url_for(
            'account.join_from_invite',
            user_id=user.id,
            token=token,
            _external=True)
        get_queue().enqueue(
            send_email,
            recipient=user.email,
            subject='You Are Invited To Join',
            template='account/email/invite',
            user=user,
            invite_link=invite_link, )
        flash('User {} successfully invited'.format(user.full_name()),
              'form-success')
    return render_template('counselor/new_user.html', form=form)


@counselor.route('/users')
@login_required
@counselor_required
def registered_users():
    """View all registered users."""
    users = User.query.all()
    roles = Role.query.all()
    return render_template(
        'counselor/registered_users.html', users=users, roles=roles)


@counselor.route('/user/<int:user_id>')
@counselor.route('/user/<int:user_id>/info')
@login_required
@counselor_required
def user_info(user_id):
    """View a user's profile."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('counselor/manage_user.html', user=user)


@counselor.route('/user/<int:user_id>/profile')
@login_required
@counselor_required
def view_user_profile(user_id):
    """ See a student's profile - containing all info from DB """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    return render_template('student/student_profile.html', user=user)


@counselor.route('/user/<int:user_id>/change-email', methods=['GET', 'POST'])
@login_required
@counselor_required
def change_user_email(user_id):
    """Change a user's email."""
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = ChangeUserEmailForm()
    if form.validate_on_submit():
        user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash('Email for user {} successfully changed to {}.'
              .format(user.full_name(), user.email), 'form-success')
    return render_template('counselor/manage_user.html', user=user, form=form)


@counselor.route('/student_database', methods=['GET'])
@login_required
@counselor_required
def student_database():
    """View student database."""
    student_profiles = StudentProfile.query.all()
    return render_template('counselor/student_database.html', student_profiles=student_profiles)


@counselor.route('/_update_editor_contents', methods=['POST'])
@login_required
@counselor_required
def update_editor_contents():
    """Update the contents of an editor."""

    edit_data = request.form.get('edit_data')
    editor_name = request.form.get('editor_name')

    editor_contents = EditableHTML.query.filter_by(
        editor_name=editor_name).first()
    if editor_contents is None:
        editor_contents = EditableHTML(editor_name=editor_name)
    editor_contents.value = edit_data

    db.session.add(editor_contents)
    db.session.commit()

    return 'OK', 200

@counselor.route('/checklist', methods=['GET', 'POST'])
@login_required
@counselor_required
def checklist():
    #display list of default checklist items and option to add a new one
    default_items = ChecklistItem.query.filter_by(creator_role_id=3)
    form = AddChecklistItemForm()
    if form.validate_on_submit():
        #create new checklist item from form data
        new_item = ChecklistItem(
                    text=form.item_text.data,
                    assignee_id=current_user.id,
                    creator_role_id=3)
        db.session.add(new_item)

        users = User.query.filter_by(role_id=1)
        for user in users:
            #add new checklist to each user's account
            checklist_item = ChecklistItem(
                assignee_id=user.id,
                text=form.item_text.data,
                is_deletable=False)
            db.session.add(checklist_item)
        db.session.commit()
        return redirect(url_for('counselor.checklist'))
    return render_template('counselor/checklist.html', form=form, checklist=default_items)
