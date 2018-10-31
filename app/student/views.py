import datetime
from flask import (abort, flash, redirect, render_template, url_for, request,
                   jsonify)
from flask_login import current_user, login_required
from ..models import TestScore, RecommendationLetter, Interest, Essay, College, Major, StudentProfile, ScattergramData, Acceptance, StudentScholarship
from .. import db, csrf
from . import student
from .forms import (
    AddTestScoreForm, AddRecommendationLetterForm, AddSupplementalEssayForm,
    EditCollegeForm, EditSupplementalEssayForm, EditTestScoreForm,
    EditCommonAppEssayForm, AddChecklistItemForm, EditChecklistItemForm,
    EditStudentProfile, AddMajorForm, AddCollegeForm,
    EditRecommendationLetterForm, AddCommonAppEssayForm,
    AddAcceptanceForm, EditAcceptanceForm, AddStudentScholarshipForm, EditStudentScholarshipForm)
from ..models import (User, College, Essay, TestScore, ChecklistItem,
                      RecommendationLetter, TestName, Notification,
                      Acceptance, Scholarship)
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import flask
import requests
import os
import datetime
from datetime import date
os.environ[
    'OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # TODO: remove before production?

import random #for fake college interest

#load student profile, test scores for profile and comparer
def load_student_profile(current_user):
    sat = 'N/A'
    act = 'N/A'
    student_profile = current_user.student_profile
    if student_profile is not None:
        test_scores = student_profile.test_scores
        for t in test_scores:
            if t.name == 'SAT':
                sat = max(sat, t.score) if sat != 'N/A' else t.score
            if t.name == 'ACT':
                act = max(act, t.score) if act != 'N/A' else t.score

    return student_profile, sat, act

@student.route('/profile')
@login_required
def view_user_profile():
    sat = 'N/A'
    act = 'N/A'
    current_user.student_profile, sat, act = load_student_profile(current_user)
    if current_user.student_profile is not None:
        return render_template(
            'student/student_profile.html',
            user=current_user,
            sat=sat,
            act=act)
    else:
        abort(404)

def load_comparer_data_col():
    colleges = (current_user.student_profile.colleges)
    return colleges
@student.route('/comparer')
@login_required
def comparer():
    student_profile, sat, act = load_student_profile(current_user)
    colleges = load_comparer_data_col()
    for col in colleges:
        interest = Interest.query.filter_by(name=col.name).first()
        try:
            col.interest = interest.lvl
        except:
            col.interest = "High"
        col.sat_score_average_overall = int(col.sat_score_average_overall)
        col.act_score_average_overall = int(col.act_score_average_overall)
        col.scatter_link = '/student/college_profile/' + str(col.id)

    return render_template('student/college_comparer.html', user=current_user, 
        act=act, sat=sat, 
        colleges=colleges, authenticated=True)

@student.route('/profile_from_id/<int:student_profile_id>')
def get_profile_from_id(student_profile_id):
    return redirect(get_redirect_url(student_profile_id))


@student.route('/calendar')
@login_required
def calendar():
    if current_user.student_profile.cal_token:
        return render_template('student/calendar.html', authenticated=True)
    else:
        return render_template('student/calendar.html', authenticated=False)


@student.route('/calendar_data', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def calendar_data():
    if not current_user.student_profile.cal_token:
        return jsonify(data=[])
    # Load credentials from the session.
    credentials_json = {
        'token': current_user.student_profile.cal_token,
        'refresh_token': current_user.student_profile.cal_refresh_token,
        'token_uri': current_user.student_profile.cal_token_uri,
        'client_id': current_user.student_profile.cal_client_id,
        'client_secret': current_user.student_profile.cal_client_secret,
        'scopes': current_user.student_profile.cal_scopes
    }
    credentials = google.oauth2.credentials.Credentials(**credentials_json)
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)

    now = datetime.datetime.utcnow()
    last_year = now.replace(
        year=now.year - 1).isoformat() + 'Z'  # 'Z' indicates UTC time
    event_data = []
    page_token = None
    while True:
        events = service.events().list(
            calendarId='primary', pageToken=page_token,
            timeMin=last_year).execute()
        for event in events['items']:
            try:
                event_data.append({
                    'title': event['summary'],
                    'start': event['start']['dateTime'],
                    'end': event['end']['dateTime']
                })
                page_token = events.get('nextPageToken')
            except KeyError:
                print("key error when parsing calendar")
        if not page_token:
            break

    current_user.student_profile.cal_token = credentials.token
    current_user.student_profile.cal_refresh_token = credentials.refresh_token
    current_user.student_profile.cal_token_uri = credentials.token_uri
    current_user.student_profile.cal_client_id = credentials.client_id
    current_user.student_profile.cal_client_secret = credentials.client_secret
    current_user.student_profile.cal_scopes = credentials.scopes
    db.session.add(current_user)
    db.session.commit()
    return jsonify(data=event_data)


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRETS_FILE = os.environ.get('CLIENT_SECRETS_FILE')


@student.route('/authorize_calendar')
@login_required
def authorize_calendar():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('student.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        prompt='consent',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    current_user.student_profile.cal_state = state
    db.session.add(current_user)
    db.session.commit()
    return redirect(authorization_url)


@student.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = current_user.student_profile.cal_state

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('student.oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in database
    credentials = flow.credentials
    current_user.student_profile.cal_token = credentials.token
    current_user.student_profile.cal_refresh_token = credentials.refresh_token
    current_user.student_profile.cal_token_uri = credentials.token_uri
    current_user.student_profile.cal_client_id = credentials.client_id
    current_user.student_profile.cal_client_secret = credentials.client_secret
    current_user.student_profile.cal_scopes = credentials.scopes
    current_user.student_profile.cal_state = state
    db.session.add(current_user)
    db.session.commit()
    add_pending_events()
    return redirect(url_for('student.calendar'))


def add_pending_events():
    # if a student had checklist items created before they authorized gcal
    checklist_items = ChecklistItem.query.filter_by(
        assignee_id=current_user.student_profile_id)
    for item in checklist_items:
        if not item.event_created:
            # add these items to their calendar
            result = add_to_cal(current_user.student_profile_id, item.text,
                                item.deadline)
            item.cal_event_id = result['event_id']
            item.event_created = result['event_created']
            db.session.add(item)
    db.session.commit()


@student.route(
    '/profile/edit/<int:student_profile_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(student_profile_id):
    # only allows the student or counselors/admins to edit a student's profile
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    # Allow user to update basic profile information.
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if student_profile:
        form = EditStudentProfile(
            grade=student_profile.grade,
            high_school=student_profile.high_school,
            phone_number=student_profile.phone_number,
            graduation_year=student_profile.graduation_year,
            district=student_profile.district,
            city=student_profile.city,
            state=student_profile.state,
            fafsa_status=student_profile.fafsa_status,
            unweighted_gpa=student_profile.unweighted_gpa,
            weighted_gpa=student_profile.weighted_gpa,
            early_deadline=bool_to_string(student_profile.early_deadline))
        if form.validate_on_submit():
            # Update user profile information.
            student_profile.grade = form.grade.data
            student_profile.high_school = form.high_school.data
            student_profile.phone_number = form.phone_number.data
            student_profile.graduation_year = form.graduation_year.data
            student_profile.district = form.district.data
            student_profile.city = form.city.data
            student_profile.state = form.state.data
            student_profile.fafsa_status = form.fafsa_status.data
            student_profile.unweighted_gpa = form.unweighted_gpa.data
            student_profile.weighted_gpa = form.weighted_gpa.data
            student_profile.early_deadline = string_to_bool(
                form.early_deadline.data)
            db.session.add(student_profile)
            db.session.commit()
            url = get_redirect_url(student_profile.id)
            return redirect(url)
        return render_template(
            'student/update_profile.html',
            form=form,
            student_profile_id=student_profile.id)
    abort(404)


# test score methods


@student.route(
    '/profile/add_test_score/<int:student_profile_id>',
    methods=['GET', 'POST'])
@login_required
def add_test_score(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    form = AddTestScoreForm()
    if form.validate_on_submit():
        # create new test score from form data
        new_item = TestScore(
            student_profile_id=student_profile_id,
            name=form.test_name.data.name,
            month=form.month.data,
            year=form.year.data,
            score=form.score.data)
        db.session.add(new_item)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Test Score",
        student_profile_id=student_profile_id)


@student.route(
    '/profile/test_score/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_test_score(item_id):
    test_score = TestScore.query.filter_by(id=item_id).first()
    if test_score:
        # only allows the student or counselors/admins to perform action
        if test_score.student_profile_id == current_user.student_profile_id or current_user.role_id != 1:
            db.session.delete(test_score)
            db.session.commit()
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})


@student.route(
    '/profile/test_score/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_test_score(item_id):
    test_score = TestScore.query.filter_by(id=item_id).first()
    if test_score:
        # only allows the student or counselors/admins to access page
        if test_score.student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        form = EditTestScoreForm(
            test_name=TestName.query.filter_by(name=test_score.name).first(),
            month=test_score.month,
            year=test_score.year,
            score=test_score.score)
        if form.validate_on_submit():
            test_score.name = form.test_name.data.name
            test_score.month = form.month.data
            test_score.year = form.year.data
            test_score.score = form.score.data
            db.session.add(test_score)
            db.session.commit()
            url = get_redirect_url(test_score.student_profile_id)
            return redirect(url)
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Test Score",
            student_profile_id=test_score.student_profile_id)
    abort(404)


def get_redirect_url(student_profile_id):
    if (current_user.is_student()
            and current_user.student_profile_id == student_profile_id):
        return url_for('student.view_user_profile')
    else:
        if (current_user.is_counselor() or current_user.is_admin()):
            student = User.query.filter_by(
                student_profile_id=student_profile_id).first()
            if student is not None:
                return url_for(
                    'counselor.view_user_profile', user_id=student.id)
    return abort(404)


# recommendation letter methods


@student.route(
    '/profile/add_recommendation_letter/<int:student_profile_id>',
    methods=['GET', 'POST'])
@login_required
def add_recommendation_letter(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    form = AddRecommendationLetterForm()
    if form.validate_on_submit():
        new_item = RecommendationLetter(
            student_profile_id=student_profile_id,
            name=form.name.data,
            category=form.category.data,
            status=form.status.data)
        db.session.add(new_item)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Recommendation Letter",
        student_profile_id=student_profile_id)


@student.route(
    '/profile/recommendation_letter/edit/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
def edit_recommendation_letter(item_id):
    letter = RecommendationLetter.query.filter_by(id=item_id).first()
    if letter:
        # only allows the student or counselors/admins to access page
        if letter.student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        form = EditRecommendationLetterForm(
            name=letter.name, category=letter.category, status=letter.status)
        if form.validate_on_submit():
            letter.name = form.name.data
            letter.category = form.category.data
            letter.status = form.status.data
            db.session.add(letter)
            db.session.commit()
            url = get_redirect_url(letter.student_profile_id)
            return redirect(url)
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Recommendation Letter",
            student_profile_id=letter.student_profile_id)
    abort(404)


@student.route(
    '/profile/recommendation_letter/delete/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_recommendation_letter(item_id):
    letter = RecommendationLetter.query.filter_by(id=item_id).first()
    if letter:
        # only allows the student or counselors/admins to perform action
        if letter.student_profile_id == current_user.student_profile_id or current_user.role_id != 1:
            db.session.delete(letter)
            db.session.commit()
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# acceptance methods


@student.route(
    '/profile/add_acceptance/<int:student_profile_id>',
    methods=['GET','POST'])
@login_required
def add_acceptance(student_profile_id):
    # only student or counselor/admin may access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    form = AddAcceptanceForm()
    if form.validate_on_submit():
        new_item = Acceptance(
            student_profile_id=student_profile_id,
            college=form.college.data.name,
            status=form.status.data,
            link=form.link.data)
        db.session.add(new_item)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Acceptance",
        student_profile_id=student_profile_id)


@student.route(
    '/profile/acceptance/edit/<int:item_id>',
    methods=['GET','POST'])
@login_required
def edit_acceptance(item_id):
    acceptance = Acceptance.query.filter_by(id=item_id).first()
    if acceptance:
        # only allows student or counselors/admin to access page
        if acceptance.student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        form = EditAcceptanceForm(
            college=acceptance.college,
            status=acceptance.status,
            link=acceptance.link)
        if form.validate_on_submit():
            acceptance.college = form.college.data.name
            acceptance.status = form.status.data
            acceptance.link = form.link.data
            db.session.add(acceptance)
            db.session.commit()
            url = get_redirect_url(acceptance.student_profile_id)
            return redirect(url)
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Acceptance",
            student_profile_id=acceptance.student_profile_id)
    abort(404)


@student.route(
    '/profile/acceptance/delete/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_acceptance(item_id):
    acceptance = Acceptance.query.filter_by(id=item_id).first()
    if acceptance:
        # only allows student or counselors/admin to access page
        if acceptance.student_profile_id == current_user.student_profile_id or current_user.role_id != 1:
            db.session.delete(acceptance)
            db.session.commit()
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# college methods


@student.route(
    '/profile/add_college/<int:student_profile_id>', methods=['GET', 'POST'])
@login_required
def add_college(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    # Add a college student is interested in.
    form = AddCollegeForm()
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if form.validate_on_submit():
        if form.name.data not in student_profile.colleges:
            student_profile.colleges.append(form.name.data)
            interest = Interest(lvl=form.lvl.data)
            interest.name = form.name.data.name
            student_profile.interests.append(interest)
            db.session.add(student_profile)
            db.session.commit()
        elif form.name.data in student_profile.colleges:
            interest = Interest.query.filter_by(name=form.name.data.name).first()
            interest.lvl = form.lvl.data

        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add College",
        student_profile_id=student_profile_id)


@student.route('/colleges')
@login_required
def colleges():
    """View all colleges."""
    colleges = College.query.all()
    return render_template('student/colleges.html', colleges=colleges)


@student.route(
    '/profile/college/delete/<int:item_id>/<int:student_profile_id>',
    methods=['POST'])
@login_required
@csrf.exempt
def delete_college(item_id, student_profile_id):
    # only allows the student or counselors/admins to perform action
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        return jsonify({"success": "False"})
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    college = College.query.filter_by(id=item_id).first()
    interest = Interest.query.filter_by(name=college.name).first()
    if college and student_profile:
        student_profile.colleges.remove(college)
        if interest is not None:
            student_profile.interests.remove(interest)
            db.session.delete(interest)
        db.session.add(student_profile)
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# scholarship methods

@student.route('/scholarships')
@login_required
def scholarships():
    """View all scholarships"""
    scholarships = Scholarship.query.all()
    return render_template('student/scholarships.html', scholarships=scholarships)



# common app essay methods


@student.route(
    '/profile/add_common_app_essay/<int:student_profile_id>',
    methods=['GET', 'POST'])
@login_required
def add_common_app_essay(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    form = AddCommonAppEssayForm()
    if form.validate_on_submit():
        student_profile = StudentProfile.query.filter_by(
            id=student_profile_id).first()
        student_profile.common_app_essay = form.link.data
        student_profile.common_app_essay_status = form.status.data
        db.session.add(student_profile)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/add_academic_info.html',
        form=form,
        student_profile_id=student_profile_id,
        header="Add Common App Essay")


@student.route(
    '/profile/common_app_essay/edit/<int:student_profile_id>',
    methods=['GET', 'POST'])
@login_required
def edit_common_app_essay(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    form = EditCommonAppEssayForm(link=student_profile.common_app_essay)
    if form.validate_on_submit():
        student_profile.common_app_essay = form.link.data
        student_profile.common_app_essay_status = form.status.data
        db.session.add(student_profile)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/edit_academic_info.html',
        form=form,
        header="Edit Common App Essay",
        student_profile_id=student_profile.id)


@student.route(
    '/profile/common_app_essay/delete/<int:student_profile_id>',
    methods=['POST'])
@login_required
@csrf.exempt
def delete_common_app_essay(student_profile_id):
    # only allows the student or counselors/admins to perform action
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if student_profile:
        student_profile.common_app_essay = ''
        student_profile.common_app_essay_status = 'Incomplete'
        db.session.add(student_profile)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    abort(404)


# supplemental essay methods


@student.route(
    '/profile/add_supplemental_essay/<int:student_profile_id>',
    methods=['GET', 'POST'])
@login_required
def add_supplemental_essay(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    form = AddSupplementalEssayForm()
    if form.validate_on_submit():
        # create new essay from form data
        new_item = Essay(
            student_profile_id=student_profile_id,
            name=form.name.data,
            link=form.link.data,
            status=form.status.data)
        db.session.add(new_item)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)

    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Supplemental Essay",
        student_profile_id=student_profile_id)


@student.route(
    '/profile/supplemental_essay/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_supplemental_essay(item_id):
    essay = Essay.query.filter_by(id=item_id).first()
    if essay:
        # only allows the student or counselors/admins to access page
        if essay.student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        form = EditSupplementalEssayForm(
            essay_name=essay.name, link=essay.link, status=essay.status)
        if form.validate_on_submit():
            essay.name = form.essay_name.data
            essay.link = form.link.data
            essay.status = form.status.data
            db.session.add(essay)
            db.session.commit()
            url = get_redirect_url(essay.student_profile_id)
            return redirect(url)
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Supplemental Essay",
            student_profile_id=essay.student_profile_id)
    abort(404)


@student.route(
    '/profile/supplemental_essay/delete/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_supplemental_essay(item_id):
    essay = Essay.query.filter_by(id=item_id).first()
    if essay:
        # only allows the student or counselors/admins to perform action
        if essay.student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
            return jsonify({"success": "False"})
        db.session.delete(essay)
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# major methods


@student.route(
    '/profile/add_major/<int:student_profile_id>', methods=['GET', 'POST'])
@login_required
def add_major(student_profile_id):
    # only allows the student or counselors/admins to access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    # Add a major student is interested in.
    form = AddMajorForm()
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if form.validate_on_submit():
        if form.major.data not in student_profile.majors:
            # Only add major if not already in their list.
            major_name = Major.query.filter_by(name=form.major.data).first()
            if major_name is not None:
                # Major already exists in database.
                student_profile.majors.append(major_name)
            else:
                student_profile.majors.append(Major(name=form.major.data))
            db.session.add(student_profile)
            db.session.commit()
            url = get_redirect_url(student_profile_id)
            return redirect(url)

    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Major",
        student_profile_id=student_profile_id)


@student.route(
    '/profile/major/delete/<int:item_id>/<int:student_profile_id>',
    methods=['POST'])
@login_required
@csrf.exempt
def delete_major(item_id, student_profile_id):
    # only allows the student or counselors/admins to perform action
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        return jsonify({"success": "False"})
    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    major = Major.query.filter_by(id=item_id).first()
    if major:
        student_profile.majors.remove(major)
        db.session.add(student_profile)
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# checklist methods


@student.route('/')
@login_required
def dashboard():
    # get the logged-in user's profile id
    if current_user.student_profile_id:
        return redirect(
            url_for(
                'student.checklist',
                student_profile_id=current_user.student_profile_id))
    else:
        return redirect(url_for('main.index'))


# order checklist items so soonest deadline is first
# checklists with no deadline appear at the end
def compare_checklist_items(item):
    if item.deadline:
        return item.deadline
    else:
        return date.max


@student.route('/checklist/<int:student_profile_id>', methods=['GET', 'POST'])
@login_required
def checklist(student_profile_id):
    # only allows the student or counselors/admins to see a student's profile
    if student_profile_id == current_user.student_profile_id or current_user.role_id != 1:
        checklist_items = ChecklistItem.query.filter_by(
            assignee_id=student_profile_id)
        completed_items = [item for item in checklist_items if item.is_checked]
        completed_items.sort(key=compare_checklist_items)
        checklist_items = [
            item for item in checklist_items if not item.is_checked
        ]
        checklist_items.sort(key=compare_checklist_items)
        #### form to add checklist item ###
        form = AddChecklistItemForm()
        if form.validate_on_submit():
            result = add_to_cal(student_profile_id, form.item_text.data,
                                form.date.data)
            # add new checklist item to user's account
            checklist_item = ChecklistItem(
                assignee_id=student_profile_id,
                text=form.item_text.data,
                is_deletable=True,
                deadline=form.date.data,
                cal_event_id=result['event_id'],
                event_created=result['event_created'])
            # if counselor is adding checklist item, send a notification
            if current_user.role_id != 1:
                notif_text = '{} {} added "{}" to your checklist'.format(
                    current_user.first_name, current_user.last_name,
                    checklist_item.text)
                notification = Notification(
                    text=notif_text, student_profile_id=student_profile_id)
                db.session.add(notification)
            db.session.add(checklist_item)
            db.session.commit()
            return redirect(
                url_for(
                    'student.checklist',
                    student_profile_id=student_profile_id))
        ### pull student notifications ###
        current_notifs = []
        if current_user.role_id == 1:
            now = datetime.datetime.utcnow()
            all_notifs = Notification.get_user_notifications(
                student_profile_id=current_user.student_profile_id)
            for n in all_notifs:
                time_diff = now - n.created_at
                if time_diff.days > 14 or n.seen:
                    db.session.delete(n)
                else:
                    ago_str = ''
                    if time_diff.days > 0:
                        ago_str = '{} days ago'.format(time_diff.days)
                    elif time_diff.seconds >= 3600:
                        hours = time_diff.seconds // 3600
                        ago_str = '1 hour ago' if hours == 1 else '{} hours ago'.format(
                            hours)
                    elif time_diff.seconds >= 60:
                        mins = time_diff.seconds // 60
                        ago_str = '1 minute ago' if mins == 1 else '{} minutes ago'.format(
                            mins)
                    else:
                        ago_str = '1 second ago' if time_diff.seconds == 1 else '{} seconds ago'.format(
                            time_diff.seconds)
                    current_notifs += [(n, ago_str)]
                    n.seen = True
            db.session.commit()
        if len(current_notifs) == 0:
            current_notifs = None
        ### return student dashboard checklist ###
        return render_template(
            'student/checklist.html',
            form=form,
            checklist=checklist_items,
            notifications=current_notifs,
            completed=completed_items,
            student_profile_id=student_profile_id)
    abort(404)


def add_to_cal(student_profile_id, text, deadline):
    if deadline is None:
        return {"event_id": "1", "event_created": False}

    student_profile = StudentProfile.query.filter_by(
        id=student_profile_id).first()
    if student_profile is None or student_profile.cal_token is None:
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
    y = deadline.year
    m = deadline.month
    d = deadline.day
    event_body = {
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

    event = service.events().insert(
        calendarId='primary', body=event_body).execute()
    student_profile.cal_token = credentials.token
    student_profile.cal_refresh_token = credentials.refresh_token
    student_profile.cal_token_uri = credentials.token_uri
    student_profile.cal_client_id = credentials.client_id
    student_profile.cal_client_secret = credentials.client_secret
    student_profile.cal_scopes = credentials.scopes
    db.session.add(student_profile)
    db.session.commit()
    return {"event_id": event.get('id'), "event_created": True}


@student.route('/checklist/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_checklist_item(item_id):
    checklist_item = ChecklistItem.query.filter_by(id=item_id).first()
    if checklist_item:
        # only allows the student or counselors/admins to perform action
        if checklist_item.assignee_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        if checklist_item.deadline is not None and checklist_item.event_created:
            delete_event(checklist_item.cal_event_id)
        db.session.delete(checklist_item)
        db.session.commit()
        return redirect(
            url_for(
                'student.checklist',
                student_profile_id=checklist_item.assignee_id))
    flash('Item could not be deleted', 'error')
    return redirect(url_for('main.index'))


def delete_event(event_id):
    token = current_user.student_profile.cal_token
    refresh_token = current_user.student_profile.cal_refresh_token
    token_uri = current_user.student_profile.cal_token_uri
    client_id = current_user.student_profile.cal_client_id
    client_secret = current_user.student_profile.cal_client_secret
    scopes = current_user.student_profile.cal_scopes
    credentials_json = {
        'token': token,
        'refresh_token': refresh_token,
        'token_uri': token_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'scopes': scopes
    }

    credentials = google.oauth2.credentials.Credentials(**credentials_json)
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)
    service.events().delete(calendarId='primary', eventId=event_id).execute()

    current_user.student_profile.cal_token = credentials.token
    current_user.student_profile.cal_refresh_token = credentials.refresh_token
    current_user.student_profile.cal_token_uri = credentials.token_uri
    current_user.student_profile.cal_client_id = credentials.client_id
    current_user.student_profile.cal_client_secret = credentials.client_secret
    current_user.student_profile.cal_scopes = credentials.scopes
    db.session.add(current_user)
    db.session.commit()


def update_event(event_id, new_text, new_deadline):
    token = current_user.student_profile.cal_token
    refresh_token = current_user.student_profile.cal_refresh_token
    token_uri = current_user.student_profile.cal_token_uri
    client_id = current_user.student_profile.cal_client_id
    client_secret = current_user.student_profile.cal_client_secret
    scopes = current_user.student_profile.cal_scopes
    credentials_json = {
        'token': token,
        'refresh_token': refresh_token,
        'token_uri': token_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'scopes': scopes
    }

    credentials = google.oauth2.credentials.Credentials(**credentials_json)
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=credentials)
    event = service.events().get(
        calendarId='primary', eventId=event_id).execute()
    event['summary'] = new_text
    y = new_deadline.year
    m = new_deadline.month
    d = new_deadline.day
    event['start'] = {
        'dateTime': datetime.datetime(y, m, d).isoformat('T'),
        'timeZone': 'America/Los_Angeles',
    }
    event['end'] = {
        'dateTime': datetime.datetime(y, m, d).isoformat('T'),
        'timeZone': 'America/Los_Angeles',
    }
    updated_event = service.events().update(
        calendarId='primary', eventId=event['id'], body=event).execute()

    current_user.student_profile.cal_token = credentials.token
    current_user.student_profile.cal_refresh_token = credentials.refresh_token
    current_user.student_profile.cal_token_uri = credentials.token_uri
    current_user.student_profile.cal_client_id = credentials.client_id
    current_user.student_profile.cal_client_secret = credentials.client_secret
    current_user.student_profile.cal_scopes = credentials.scopes
    db.session.add(current_user)
    db.session.commit()


@student.route('/checklist/complete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def complete_checklist_item(item_id):
    checklist_item = ChecklistItem.query.filter_by(id=item_id).first()
    if checklist_item:
        # only allows the student or counselors/admins to access page
        if checklist_item.assignee_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        checklist_item.is_checked = True
        db.session.add(checklist_item)
        db.session.commit()
        return redirect(
            url_for(
                'student.checklist',
                student_profile_id=checklist_item.assignee_id))
    flash('Item could not be completed', 'error')
    return redirect(url_for('main.index'))


@student.route('/checklist/undo/<int:item_id>', methods=['GET', 'POST'])
@login_required
def undo_checklist_item(item_id):
    checklist_item = ChecklistItem.query.filter_by(id=item_id).first()
    if checklist_item:
        # only allows the student or counselors/admins to access page
        if checklist_item.assignee_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        checklist_item.is_checked = False
        db.session.add(checklist_item)
        db.session.commit()
        return redirect(
            url_for(
                'student.checklist',
                student_profile_id=checklist_item.assignee_id))
    flash('Item could not be undone', 'error')
    return redirect(url_for('main.index'))


@student.route('/checklist/update/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_checklist_item(item_id):
    item = ChecklistItem.query.filter_by(id=item_id).first()
    if item:
        # only allows the student or counselors/admins to access page
        if item.assignee_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        form = EditChecklistItemForm(item_text=item.text, date=item.deadline)
        if form.validate_on_submit():
            if item.deadline is not None and form.date.data is not None:
                update_event(item.cal_event_id, form.item_text.data,
                             form.date.data)
            else:
                if item.deadline is None and form.date.data is not None:
                    add_to_cal(item.assignee_id, form.item_text.data,
                               form.date.data)
            item.text = form.item_text.data
            item.deadline = form.date.data
            db.session.add(item)
            db.session.commit()
            return redirect(
                url_for(
                    'student.checklist', student_profile_id=item.assignee_id))
        return render_template(
            'student/update_checklist.html',
            form=form,
            student_profile_id=item.assignee_id)
    flash('Item could not be updated', 'error')
    return redirect(url_for('main.index'))


@student.route('/college_profile/<int:college_id>')
@login_required
def view_college_profile(college_id):
    college = College.query.filter_by(id=college_id).first()
    return render_template(
        'main/college_profile.html',
        pageType='college_profile',
        college=college)

@student.route('/scholarship_profile/<int:scholarship_id>')
@login_required
def view_scholarship_profile(scholarship_id):
    scholarship = Scholarship.query.filter_by(id=scholarship_id).first()
    return render_template(
        'main/scholarship_profile.html', pageType='scholarship_profile', scholarship=scholarship)


def string_to_bool(str):
    if str == 'True':
        return True
    if str == 'False':
        return False


def bool_to_string(bool):
    if bool:
        return 'True'
    else:
        return 'False'


@csrf.exempt
@student.route('/acceptance/<int:item_id>/<int:student_profile_id>', methods=['GET', 'POST'])
@login_required
def view_acceptance_profile(item_id, student_profile_id):
    acceptance = Acceptance.query.filter_by(id=item_id).first()
    if acceptance:
        college = College.query.filter_by(name=acceptance.college).first()
        student = StudentProfile.query.filter_by(id=student_profile_id).first()
        return render_template(
            'student/acceptance_profile.html',
            acceptance=acceptance, 
            college=college,
            student_profile=student)
    abort(404)

@csrf.exempt
@student.route('/profile/add_scholarship/<int:student_profile_id>', methods=['GET','POST'])
@login_required
def add_student_scholarship(student_profile_id):
    # only student or counselor admin may access page
    if student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
        abort(404)
    form = AddStudentScholarshipForm()
    if form.validate_on_submit():
        new_item = StudentScholarship(
            student_profile_id=student_profile_id,
            name=form.name.data,
            award_amount=form.award_amount.data)
        student = StudentProfile.query.filter_by(id=student_profile_id).first()
        student.scholarship_amount = student.scholarship_amount + form.award_amount.data
        db.session.add(new_item)
        db.session.commit()
        url = get_redirect_url(student_profile_id)
        return redirect(url)
    return render_template(
        'student/add_academic_info.html',
        form=form,
        header='Add Student Scholarship',
        student_profile_id=student_profile_id)

@student.route(
    '/profile/student_scholarship/edit/<int:item_id>', 
    methods=['GET','POST'])
@login_required
def edit_student_scholarship(item_id):
    schol = StudentScholarship.query.filter_by(id=item_id).first()
    student = StudentProfile.query.filter_by(id=schol.student_profile_id).first()    
    if schol:
        if schol.student_profile_id != current_user.student_profile_id and current_user.role_id == 1:
            abort(404)
        form = EditStudentScholarshipForm(
            name=schol.name,
            award_amount=schol.award_amount
        )
        student.scholarship_amount = student.scholarship_amount - schol.award_amount
        if form.validate_on_submit():
            schol.name = form.name.data
            schol.award_amount = form.award_amount.data
            student.scholarship_amount = student.scholarship_amount + form.award_amount.data
            db.session.add(schol)
            db.session.commit()
            url = get_redirect_url(schol.student_profile_id)
            return redirect(url)
        student.scholarship_amount = student.scholarship_amount + schol.award_amount        
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Student Scholarship",
            student_profile_id=schol.student_profile_id)
    abort(404)

@student.route(
    '/profile/student_scholarship/delete/<int:item_id>',
    methods=['GET','POST'])
@login_required
@csrf.exempt
def delete_student_scholarship(item_id):
    schol = StudentScholarship.query.filter_by(id=item_id).first()
    student = StudentProfile.query.filter_by(id=schol.student_profile_id).first()
    if schol:
        if schol.student_profile_id == current_user.student_profile_id or current_user.role_id != 1:
            student.scholarship_amount = student.scholarship_amount - schol.award_amount
            db.session.delete(schol)
            db.session.commit()
            return jsonify({"success": "True"})
    return jsonify({"success": "False"})