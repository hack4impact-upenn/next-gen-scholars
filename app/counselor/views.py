from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from flask_rq import get_queue

from .forms import (ChangeAccountTypeForm, ChangeUserEmailForm, InviteUserForm,
                    NewUserForm, AddChecklistItemForm, AddTestNameForm, EditTestNameForm,
                    DeleteTestNameForm, AddCollegeProfileForm, EditCollegeProfileStep1Form,
                    EditCollegeProfileStep2Form, DeleteCollegeProfileForm)
from . import counselor
from .. import db
from ..decorators import counselor_required
from ..decorators import admin_required
from ..email import send_email
from ..models import (Role, User, College, StudentProfile,
                      EditableHTML, ChecklistItem, TestName, College, Notification)


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
            invite_link=invite_link,
        )
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

@counselor.route('/colleges')
@login_required
@counselor_required
def colleges():
    """View all colleges."""
    colleges = College.query.all()
    return render_template(
        'counselor/colleges.html', colleges=colleges)

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
    if not user.is_student():
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
        flash('Email for user {} successfully changed to {}.'.format(
            user.full_name(), user.email), 'form-success')
    return render_template('counselor/manage_user.html', user=user, form=form)


@counselor.context_processor
def processor():
    def get_essay_statuses(student_profile):
        return list(set([e.status for e in student_profile.essays]))

    def get_colleges(student_profile):
        return ';'.join([c.name for c in student_profile.colleges])

    return dict(
        get_essay_statuses=get_essay_statuses, get_colleges=get_colleges)


@counselor.route('/student-database', methods=['GET', 'POST'])
@login_required
@counselor_required
def student_database():
    """View student database."""
    checklist_form = AddChecklistItemForm()
    if checklist_form.validate_on_submit():
        print(checklist_form.assignee_ids.data)
        for assignee_id in checklist_form.assignee_ids.data.split(','):
            checklist_item = ChecklistItem(
                text=checklist_form.item_text.data,
                assignee_id=assignee_id,
                is_deletable=False,
                creator_role_id=3,
                deadline=checklist_form.date.data)
            db.session.add(checklist_item)
            notif_text = '{} {} added "{}" to your checklist'.format(
                current_user.first_name, current_user.last_name, checklist_item.text)
            notification = Notification(text=notif_text, student_profile_id=assignee_id)
            db.session.add(notification)
        db.session.commit()
        flash('Checklist item added.', 'form-success')
        return redirect(url_for('counselor.student_database'))

    student_profiles = StudentProfile.query.all()
    colleges = College.query.all()
    essay_statuses = ['Incomplete', 'Waiting', 'Reviewed', 'Edited', 'Done']
    return render_template(
        'counselor/student_database.html',
        student_profiles=student_profiles,
        checklist_form=checklist_form,
        colleges=colleges,
        essay_statuses=essay_statuses)


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
    # display list of default checklist items and option to add a new one
    default_items = ChecklistItem.query.filter_by(creator_role_id=3)
    form = AddChecklistItemForm()
    if form.validate_on_submit():
        # create new checklist item from form data
        new_item = ChecklistItem(
            text=form.item_text.data,
            assignee_id=current_user.id,
            creator_role_id=3)
        db.session.add(new_item)

        users = User.query.filter_by(role_id=1)
        for user in users:
            # add new checklist to each user's account
            checklist_item = ChecklistItem(
                assignee_id=user.student_profile_id,
                text=form.item_text.data,
                is_deletable=False)
            db.session.add(checklist_item)
        db.session.commit()
        return redirect(url_for('counselor.checklist'))
    return render_template(
        'counselor/checklist.html', form=form, checklist=default_items)


@counselor.route('/calendar')
@login_required
@counselor_required
def calendar():
    """ See a calendar """
    return render_template('counselor/calendar.html')


@counselor.route('/add_test', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_test_name():
    # Allows a counselor to add a test name to the database.
    form = AddTestNameForm()
    if form.validate_on_submit():
        test_name = TestName.query.filter_by(name=form.name.data).first()
        if test_name is None:
            # Test didn't already exist in database, so add it.
            test = TestName(name=form.name.data)
            db.session.add(test)
            db.session.commit()
        else:
            flash('Test could not be added - already existed in database.', 'error')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/add_test_name.html', form=form)


@counselor.route('/edit_test', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_test_name():
    # Allows a counselor to edit a test name in the database.
    form = EditTestNameForm()
    if form.validate_on_submit():
        test_name = form.old_test.data
        test_name.name = form.new_name.data
        db.session.add(test_name)
        db.session.commit()
        flash('Test name successfully edited.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/edit_test_name.html', form=form, header='Edit Test Name')


@counselor.route('/delete_test', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_test_name():
    # Allows a counselor to delete a test name in the database.
    form = DeleteTestNameForm()
    if form.validate_on_submit():
        test_name = form.old_test.data
        db.session.delete(test_name)
        db.session.commit()
        flash('Test name successfully deleted.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/delete_test_name.html', form=form, header='Delete Test Name')


@counselor.route('/add_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_college():
    # Allows a counselor to add a college profile.
    form = AddCollegeProfileForm()
    if form.validate_on_submit():
        name = College.query.filter_by(name=form.name.data).first()
        if name is None:
            # College didn't already exist in database, so add it.
            college = College(
                name=form.name.data,
                description=form.description.data,
                early_deadline=form.early_deadline.data,
                regular_deadline=form.regular_deadline.data
            )
            db.session.add(college)
            db.session.commit()
        else:
            flash('College could not be added - already existed in database.', 'error')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/add_college.html', form=form, header='Add College Profile')


@counselor.route('/edit_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_college_step1():
    # Allows a counselor to choose which college they want to edit.
    form = EditCollegeProfileStep1Form()
    if form.validate_on_submit():
        college = College.query.filter_by(name=form.name.data.name).first()
        return redirect(url_for('counselor.edit_college_step2', college_id=college.id))
    return render_template('counselor/edit_college.html', form=form, header='Edit College Profile')


@counselor.route('/edit_college/<int:college_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_college_step2(college_id):
    # Allows a counselor to edit the previously chosen college.
    # This page is one you get re-routed to, not one that's findable.
    old_college = College.query.filter_by(id=college_id).first()
    form = EditCollegeProfileStep2Form(
        name=old_college.name,
        description=old_college.description,
        regular_deadline=old_college.regular_deadline,
        early_deadline=old_college.early_deadline)
    if form.validate_on_submit():
        college = old_college
        college.name = form.name.data
        college.description = form.description.data
        college.early_deadline = form.early_deadline.data
        college.regular_deadline = form.regular_deadline.data
        db.session.add(college)
        db.session.commit()
        flash('College profile successfully edited.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/edit_college.html', form=form, header='Edit College Profile')


@counselor.route('/delete_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_college():
    # Allows a counselor to delete a college profile.
    form = DeleteCollegeProfileForm()
    if form.validate_on_submit():
        college = form.name.data
        db.session.delete(college)
        db.session.commit()
        flash('College profile successfully deleted.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template('counselor/delete_college.html', form=form, header='Delete College Profile')
