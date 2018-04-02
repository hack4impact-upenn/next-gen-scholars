import datetime
from datetime import date
import pytz
from flask import abort, flash, redirect, render_template, url_for, request, jsonify
from flask_login import current_user, login_required
from flask_rq import get_queue
from .. import csrf
from .forms import (ChangeAccountTypeForm, ChangeUserEmailForm, InviteUserForm,
                    NewUserForm, AddChecklistItemForm, AddTestNameForm,
                    EditTestNameForm, DeleteTestNameForm,
                    AddCollegeProfileForm, EditCollegeProfileStep1Form,
                    EditCollegeProfileStep2Form, DeleteCollegeProfileForm,
                    NewSMSAlertForm, EditSMSAlertForm)
from . import counselor
from .. import db
from ..decorators import counselor_required
from ..decorators import admin_required
from ..email import send_email
from ..models import (Role, User, College, StudentProfile, EditableHTML,
                      ChecklistItem, TestName, College, Notification, SMSAlert,
                      ScattergramData)
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import requests
import os
import datetime
import csv
import io
# TODO: remove before production?
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


@counselor.route('/')
@login_required
@counselor_required
def index():
    """Counselor dashboard page."""
    return render_template('counselor/index.html')


@counselor.route('/colleges')
@login_required
@counselor_required
def colleges():
    """View all colleges."""
    colleges = College.query.all()
    return render_template('counselor/colleges.html', colleges=colleges)


@csrf.exempt
@counselor.route('/upload_colleges', methods=['GET', 'POST'])
@login_required
@counselor_required
def upload_college_file():
    if request.method == 'POST':
        f = request.files['file']

        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        header_row = True
        for row in csv_input:
            if header_row:
                header_row = False
                continue
            if len(row) >= 8 and any(row):
                # check that there are at least for columns
                # and the row is not completely blank
                college_data = College(
                    name=row[0],
                    description=row[1],
                    regular_deadline=datetime.datetime.strptime(
                        row[2], "%m/%d/%y") if row[2] else None,
                    early_deadline=datetime.datetime.strptime(
                        row[3], "%m/%d/%y") if row[3] else None,
                    fafsa_deadline=datetime.datetime.strptime(
                        row[4], "%m/%d/%y") if row[4] else None,
                    acceptance_deadline=datetime.datetime.strptime(
                        row[5], "%m/%d/%y") if row[5] else None,
                    scholarship_deadline=datetime.datetime.strptime(
                        row[6], "%m/%d/%y") if row[6] else None,
                    image = row[7]
                )
            db.session.add(college_data)
        db.session.commit()
        return redirect(url_for('counselor.colleges'))
    return render_template('counselor/upload_colleges.html')


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
    if user.is_admin():
        abort(404)
    if not user.is_student():
        abort(404)
    sat = 'N/A'
    act = 'N/A'
    student_profile = user.student_profile
    if student_profile is not None:
        test_scores = student_profile.test_scores
        for t in test_scores:
            if t.name == 'SAT':
                sat = max(sat, t.score) if sat != 'N/A' else t.score
            if t.name == 'ACT':
                act = max(act, t.score) if act != 'N/A' else t.score
        return render_template(
            'student/student_profile.html', user=user, sat=sat, act=act)
    else:
        abort(404)


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


@counselor.route('/student_database', methods=['GET', 'POST'])
@login_required
@counselor_required
def student_database():
    """View student database."""
    checklist_form = AddChecklistItemForm()
    if checklist_form.validate_on_submit():
        for assignee_id in checklist_form.assignee_ids.data.split(','):
            result = add_to_cal(
                student_profile_id=assignee_id,
                text=checklist_form.item_text.data,
                deadline=checklist_form.date.data)
            checklist_item = ChecklistItem(
                text=checklist_form.item_text.data,
                assignee_id=assignee_id,
                is_deletable=False,
                creator_role_id=3,
                deadline=checklist_form.date.data,
                cal_event_id=result['event_id'],
                event_created=result['event_created'])
            db.session.add(checklist_item)
            notif_text = '{} {} added "{}" to your checklist'.format(
                current_user.first_name, current_user.last_name,
                checklist_item.text)
            notification = Notification(
                text=notif_text, student_profile_id=assignee_id)
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


def add_to_cal(student_profile_id, text, deadline):
    # only add checklist items with a deadline to students calendar
    if deadline is None:
        return {"event_id": "1", "event_created": False}
    y = deadline.year
    m = deadline.month
    d = deadline.day
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if student_profile is None:
        return {"event_id": "1", "event_created": False}
    # if a student has not authorized google calendar yet
    if student_profile.cal_token is None:
        return {"event_id": "1", "event_created": False}
    credentials_json = {
        'token': student_profile.cal_token,
        'refresh_token': student_profile.cal_refresh_token,
        'token_uri': student_profile.cal_token_uri,
        'client_id': student_profile.cal_client_id,
        'client_secret': student_profile.cal_client_secret,
        'scopes': student_profile.cal_scopes
    }

    credentials = google.oauth2.credentials.Credentials(**credentials_json)
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)
    event = {
        'summary': text,
        'start': {
            'dateTime': datetime.datetime(y, m, d).isoformat('T'),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': datetime.datetime(y, m, d).isoformat('T'),
            'timeZone': 'America/Los_Angeles',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    # save the authentication values in case they have been refreshed
    student_profile.cal_token = credentials.token
    student_profile.cal_refresh_token = credentials.refresh_token
    student_profile.cal_token_uri = credentials.token_uri
    student_profile.cal_client_id = credentials.client_id
    student_profile.cal_client_secret = credentials.client_secret
    student_profile.cal_scopes = credentials.scopes
    db.session.add(student_profile)
    db.session.commit()
    return {"event_id": event.get('id'), "event_created": True}


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


# order checklist items, soonest deadline is first
# checklists with no deadline appear at the end
def compare_checklist_items(item):
    if item.deadline:
        return item.deadline
    else:
        return date.max


@counselor.route('/default_checklist', methods=['GET', 'POST'])
@login_required
@counselor_required
def default_checklist():
    # display list of default checklist items and option to add a new one
    default_items = ChecklistItem.query.filter_by(is_default_item=True)
    default_items = [item for item in default_items]
    default_items.sort(key=compare_checklist_items)
    form = AddChecklistItemForm()
    if form.validate_on_submit():
        # create new checklist item from form data
        new_item = ChecklistItem(
            text=form.item_text.data,
            assignee_id=current_user.id,
            creator_role_id=3,
            is_default_item=True,
            deadline=form.date.data)
        db.session.add(new_item)

        users = User.query.filter_by(role_id=1)
        for user in users:
            # add new checklist to each user's account
            checklist_item = ChecklistItem(
                assignee_id=user.student_profile_id,
                text=form.item_text.data,
                is_deletable=False,
                deadline=form.date.data)
            db.session.add(checklist_item)
        db.session.commit()
        return redirect(url_for('counselor.default_checklist'))
    return render_template(
        'counselor/default_checklist.html', form=form, checklist=default_items)


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
            flash('Test could not be added - already existed in database.',
                  'error')
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
    return render_template(
        'counselor/edit_test_name.html', form=form, header='Edit Test Name')


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
    return render_template(
        'counselor/delete_test_name.html',
        form=form,
        header='Delete Test Name')


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
                regular_deadline=form.regular_deadline.data,
                scholarship_deadline=form.scholarship_deadline.data,
                fafsa_deadline=form.fafsa_deadline.data,
                acceptance_deadline=form.acceptance_deadline.data,
                image = form.image.data)
            db.session.add(college)
            db.session.commit()
        else:
            flash('College could not be added - already existed in database.',
                  'error')
        return redirect(url_for('counselor.index'))
    return render_template(
        'counselor/add_college.html', form=form, header='Add College Profile')


@counselor.route('/edit_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_college_step1():
    # Allows a counselor to choose which college they want to edit.
    form = EditCollegeProfileStep1Form()
    if form.validate_on_submit():
        college = College.query.filter_by(name=form.name.data.name).first()
        return redirect(
            url_for('counselor.edit_college_step2', college_id=college.id))
    return render_template(
        'counselor/edit_college.html',
        form=form,
        header='Edit College Profile')


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
        early_deadline=old_college.early_deadline,
        scholarship_deadline=old_college.scholarship_deadline,
        fafsa_deadline=old_college.fafsa_deadline,
        acceptance_deadline=old_college.acceptance_deadline,
        image = old_college.image)
    if form.validate_on_submit():
        college = old_college
        college.name = form.name.data
        college.description = form.description.data
        college.early_deadline = form.early_deadline.data
        college.regular_deadline = form.regular_deadline.data
        college.scholarship_deadline = form.scholarship_deadline.data
        college.fafsa_deadline = form.fafsa_deadline.data
        college.acceptance_deadline = form.acceptance_deadline.data
        college.image = form.image.data
        db.session.add(college)
        db.session.commit()
        flash('College profile successfully edited.', 'form-success')
        return redirect(url_for('counselor.colleges'))
    return render_template(
        'counselor/edit_college.html',
        form=form,
        header='Edit College Profile')


@counselor.route('/delete_college', methods=['GET', 'POST'])
@login_required
@counselor_required
def delete_college():
    """Allows a counselor to delete a college profile."""
    form = DeleteCollegeProfileForm()
    if form.validate_on_submit():
        college = form.name.data
        db.session.delete(college)
        db.session.commit()
        flash('College profile successfully deleted.', 'form-success')
        return redirect(url_for('counselor.index'))
    return render_template(
        'counselor/delete_college.html',
        form=form,
        header='Delete College Profile')


@counselor.route('/alerts', methods=['GET', 'POST'])
@login_required
@counselor_required
def alerts_dashboard():
    """Dashboard to view and add SMS alerts."""
    return render_template('counselor/alerts/alerts_dashboard.html')


@counselor.route('/alerts/manage', methods=['GET', 'POST'])
@login_required
@counselor_required
def manage_alerts():
    """Database of text notifications to send."""
    alerts = SMSAlert.query.order_by(SMSAlert.date).all()
    return render_template(
        'counselor/alerts/manage_alerts.html', alerts=alerts)


@counselor.route('/alerts/add', methods=['GET', 'POST'])
@login_required
@counselor_required
def add_alert():
    """View add alert form."""
    form = NewSMSAlertForm()
    if form.validate_on_submit():
        hour, minute = form.time.data.split(':')
        am_pm = form.am_pm.data
        hour = (int(hour) % 12) + (12 if am_pm == 'AM' else 0)
        alert = SMSAlert(
            title=form.title.data,
            content=form.content.data,
            date=form.date.data,
            time=datetime.time(hour, int(minute)))
        db.session.add(alert)
        db.session.commit()
        flash('Successfully created alert "{}"!'.format(alert.title),
              'form-success')
        return redirect(url_for('counselor.add_alert'))
    return render_template('counselor/alerts/add_alert.html', form=form)


@counselor.route('/alerts/edit/<int:alert_id>', methods=['GET', 'POST'])
@login_required
@counselor_required
def edit_alert(alert_id):
    """Edit alert."""
    alert = SMSAlert.query.filter_by(id=alert_id).first()
    if alert is None:
        abort(404)
    form = EditSMSAlertForm(
        title=alert.title,
        content=alert.content,
        date=alert.date,
        time=alert.time.strftime("%-I:%M"),
        am_pm=alert.time.strftime("%p"))
    if form.validate_on_submit():
        hour, minute = form.time.data.split(':')
        am_pm = form.am_pm.data
        hour = (int(hour) % 12) + (12 if am_pm == 'AM' else 0)
        alert.title = form.title.data
        alert.content = form.content.data
        alert.date = form.date.data
        alert.time = datetime.time(hour, int(minute))
        db.session.add(alert)
        db.session.commit()
        flash('Successfully edit alert "{}"!'.format(alert.title),
              'form-success')
        return redirect(url_for('counselor.edit_alert', alert_id=alert.id))
    return render_template('counselor/alerts/edit_alert.html', form=form)


@csrf.exempt
@counselor.route('/upload_scattergram', methods=['GET', 'POST'])
@login_required
@counselor_required
def upload_scattergram():
    if request.method == 'POST':
        try:
            f = request.files['file']
            contents = f.read()
            lines = contents.split('\r'.encode('utf-8'))
            college_names = set()
            for line in lines[1:]:
                line = line.split(','.encode('utf-8'))
                college_names.add(str(line[1], 'utf-8').strip())
                point = ScattergramData(
                    name=str(line[0], 'utf-8').strip(),
                    college=str(line[1], 'utf-8').strip(),
                    status=str(line[2], 'utf-8').strip(),
                    GPA=str(line[3], 'utf-8').strip(),
                    SAT2400=str(line[4], 'utf-8').strip(),
                    SAT1600=str(line[5], 'utf-8').strip(),
                    ACT=str(line[6], 'utf-8').strip()
                )
                db.session.add(point)
            db.session.commit()
            for name in list(college_names):
                college = College.query.filter_by(name=name).first()
                if college:
                    college.update_plots()
            message, message_type = 'Upload successful!', 'positive'
        except:
            message, message_type = 'Error with upload. Please make sure the format of the CSV file matches the description.', 'negative'
        return render_template('counselor/upload_scattergram.html', message=message, message_type=message_type)
    return render_template('counselor/upload_scattergram.html', message=None, message_type=None)
