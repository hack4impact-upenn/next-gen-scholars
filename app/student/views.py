from flask import (abort, flash, redirect, render_template, url_for, request,
                   jsonify)
from flask_login import current_user, login_required
from ..models import TestScore, RecommendationLetter, Essay, College, Major
from .. import db, csrf
from . import student
from .forms import (
    AddTestScoreForm, AddRecommendationLetterForm, AddSupplementalEssayForm,
    EditCollegeForm, EditSupplementalEssayForm, EditTestScoreForm,
    EditCommonAppEssayForm, AddChecklistItemForm, EditChecklistItemForm,
    EditStudentProfile, AddMajorForm, AddCollegeForm,
    EditRecommendationLetterForm, AddCommonAppEssayForm)
from ..models import (User, College, Essay, TestScore, ChecklistItem,
                      RecommendationLetter)


@student.route('/profile')
@login_required
def view_user_profile():
    return render_template('student/student_profile.html', user=current_user)


@student.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Allow user to update basic profile information.
    student_profile = current_user.student_profile
    if student_profile:
        form = EditStudentProfile(
            grade=student_profile.grade,
            high_school=student_profile.high_school,
            graduation_year=student_profile.graduation_year,
            district=student_profile.district,
            city=student_profile.city,
            state=student_profile.state,
            fafsa_status=student_profile.fafsa_status,
            gpa=student_profile.gpa,
            early_deadline=bool_to_string(student_profile.early_deadline))
        if form.validate_on_submit():
            # Update user profile information.
            student_profile.grade = form.grade.data
            student_profile.high_school = form.high_school.data
            student_profile.graduation_year = form.graduation_year.data
            student_profile.district = form.district.data
            student_profile.city = form.city.data
            student_profile.state = form.state.data
            student_profile.fafsa_status = form.fafsa_status.data
            student_profile.gpa = form.gpa.data
            student_profile.early_deadline = string_to_bool(
                form.early_deadline.data)
            db.session.add(student_profile)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template('student/update_profile.html', form=form)
    flash('Profile could not be updated.', 'error')
    return redirect(url_for('student.view_user_profile'))


# test score methods


@student.route('/profile/add_test_score', methods=['GET', 'POST'])
@login_required
def add_test_score():
    form = AddTestScoreForm()
    if form.validate_on_submit():
        # create new test score from form data
        new_item = TestScore(
            student_profile_id=current_user.student_profile_id,
            name=form.test_name.data,
            month=form.month.data,
            year=form.year.data,
            score=form.score.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))
    return render_template(
        'student/add_academic_info.html', form=form, header="Add Test Score")


@student.route(
    '/profile/test_score/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_test_score(item_id):
    test_score = TestScore.query.filter_by(id=item_id).first()
    if test_score:
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
        form = EditTestScoreForm(
            test_name=test_score.name,
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
            return redirect(url_for('student.view_user_profile'))
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Test Score")
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))


# recommendation letter methods


@student.route('/profile/add_recommendation_letter', methods=['GET', 'POST'])
@login_required
def add_recommendation_letter():
    # display list of default checklist items and option to add a new one
    form = AddRecommendationLetterForm()
    if form.validate_on_submit():
        # create new test score from form data
        new_item = RecommendationLetter(
            student_profile_id=current_user.student_profile_id,
            name=form.name.data,
            category=form.category.data,
            status=form.status.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))

    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Recommendation Letter")


@student.route(
    '/profile/recommendation_letter/edit/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
def edit_recommendation_letter(item_id):
    letter = RecommendationLetter.query.filter_by(id=item_id).first()
    if letter:
        form = EditRecommendationLetterForm(
            name=letter.name, category=letter.category, status=letter.status)
        if form.validate_on_submit():
            letter.name = form.name.data
            letter.category = form.category.data
            letter.status = form.status.data
            db.session.add(letter)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Recommendation Letter")
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))


@student.route(
    '/profile/recommendation_letter/delete/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_recommendation_letter(item_id):
    letter = RecommendationLetter.query.filter_by(id=item_id).first()
    if letter:
        db.session.delete(letter)
        db.session.commit()
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# college methods


@student.route('/profile/add_college', methods=['GET', 'POST'])
@login_required
def add_college():
    # Add a college student is interested in.
    form = AddCollegeForm()
    student_profile = current_user.student_profile
    if form.validate_on_submit():
        if form.name.data not in student_profile.colleges:
            # Only check to add college if not already in their list.
            college_name = College.query.filter_by(name=form.name.data).first()
            if college_name is not None:
                # College already exists in database.
                student_profile.colleges.append(college_name)
            else:
                student_profile.colleges.append(College(name=form.name.data))
            db.session.add(student_profile)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))

    return render_template(
        'student/add_academic_info.html', form=form, header="Add College")


@student.route('/profile/college/delete/<int:item_id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_college(item_id):
    college = College.query.filter_by(id=item_id).first()
    if college:
        db.session.delete(college)
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


@student.route('/profile/college/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_college(item_id):
    college = College.query.filter_by(id=item_id).first()
    if college:
        form = EditCollegeForm(college_name=college.name)
        if form.validate_on_submit():
            college.name = form.college_name.data
            db.session.add(college)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit College")
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))


# common app essay methods


@student.route('/profile/add_common_app_essay', methods=['GET', 'POST'])
@login_required
def add_common_app_essay():
    form = AddCommonAppEssayForm()
    if form.validate_on_submit():
        current_user.student_profile.common_app_essay = form.link.data
        current_user.student_profile.common_app_essay_status = form.status.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))

    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Supplemental Essay")


@student.route('/profile/common_app_essay/edit', methods=['GET', 'POST'])
@login_required
def edit_common_app_essay():
    form = EditCommonAppEssayForm(
        link=current_user.student_profile.common_app_essay)
    if form.validate_on_submit():
        current_user.student_profile.common_app_essay = form.link.data
        current_user.student_profile.common_app_essay_status = form.status.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))
    return render_template(
        'student/edit_academic_info.html',
        form=form,
        header="Edit Common App Essay")


@student.route('/profile/common_app_essay/delete', methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_common_app_essay():
    current_user.student_profile.common_app_essay = ''
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('student.view_user_profile'))


# supplemental essay methods


@student.route('/profile/add_supplemental_essay', methods=['GET', 'POST'])
@login_required
def add_supplemental_essay():
    form = AddSupplementalEssayForm()
    if form.validate_on_submit():
        # create new essay from form data
        new_item = Essay(
            student_profile_id=current_user.student_profile_id,
            name=form.name.data,
            link=form.link.data,
            status=form.status.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))

    return render_template(
        'student/add_academic_info.html',
        form=form,
        header="Add Supplemental Essay")


@student.route(
    '/profile/supplemental_essay/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_supplemental_essay(item_id):
    essay = Essay.query.filter_by(id=item_id).first()
    if essay:
        form = EditSupplementalEssayForm(
            essay_name=essay.name, link=essay.link)
        if form.validate_on_submit():
            essay.name = form.essay_name.data
            essay.link = form.link.data
            essay.status = form.status.data
            db.session.add(essay)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template(
            'student/edit_academic_info.html',
            form=form,
            header="Edit Supplemental Essay")
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))


@student.route(
    '/profile/supplemental_essay/delete/<int:item_id>',
    methods=['GET', 'POST'])
@login_required
@csrf.exempt
def delete_supplemental_essay(item_id):
    essay = Essay.query.filter_by(id=item_id).first()
    if essay:
        db.session.delete(essay)
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# major methods


@student.route('/profile/add_major', methods=['GET', 'POST'])
@login_required
def add_major():
    # Add a major student is interested in.
    form = AddMajorForm()
    student_profile = current_user.student_profile
    if form.validate_on_submit():
        if form.major.data not in student_profile.majors:
            # Only check to add major if not already in their list.
            major_name = Major.query.filter_by(name=form.major.data).first()
            if major_name is not None:
                # Major already exists in database.
                student_profile.majors.append(major_name)
            else:
                student_profile.majors.append(Major(name=form.major.data))
            db.session.add(student_profile)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))

    return render_template(
        'student/add_academic_info.html', form=form, header="Add Major")


@student.route('/profile/major/delete/<int:item_id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_major(item_id):
    major = Major.query.filter_by(id=item_id).first()
    if major:
        db.session.delete(major)
        db.session.commit()
        return jsonify({"success": "True"})
    return jsonify({"success": "False"})


# checklist methods


@student.route('/checklist/<int:student_profile_id>', methods=['GET', 'POST'])
@login_required
def checklist(student_profile_id):
    #only allows the student or counselors/admins to see a student's profile
    if student_profile_id == current_user.student_profile_id or current_user.role_id != 1:
        checklist_items = ChecklistItem.query.filter_by(
            assignee_id=student_profile_id)
        completed_items = [item for item in checklist_items if item.is_checked]
        checklist_items = [
            item for item in checklist_items if not item.is_checked
        ]
        form = AddChecklistItemForm()
        if form.validate_on_submit():
            #add new checklist item to user's account
            checklist_item = ChecklistItem(
                assignee_id=student_profile_id,
                text=form.item_text.data,
                is_deletable=True,
                deadline=form.date.data)
            db.session.add(checklist_item)
            db.session.commit()
            return redirect(
                url_for(
                    'student.checklist',
                    student_profile_id=student_profile_id))
        return render_template(
            'student/checklist.html',
            form=form,
            checklist=checklist_items,
            completed=completed_items,
            student_profile_id=student_profile_id)
    flash('You do not have access to this page', 'error')
    return redirect(url_for('main.index'))


@student.route('/checklist/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_checklist_item(item_id):
    checklist_item = ChecklistItem.query.filter_by(id=item_id).first()
    if checklist_item:
        db.session.delete(checklist_item)
        db.session.commit()
        return redirect(
            url_for(
                'student.checklist',
                student_profile_id=checklist_item.assignee_id))
    flash('Item could not be deleted', 'error')
    return redirect(url_for('main.index'))


@student.route('/checklist/complete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def complete_checklist_item(item_id):
    checklist_item = ChecklistItem.query.filter_by(id=item_id).first()
    if checklist_item:
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
        form = EditChecklistItemForm(item_text=item.text, date=item.deadline)
        if form.validate_on_submit():
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
    sat = '––'
    act = '––'
    student_profile = current_user.student_profile
    if student_profile is not None:
        test_scores = student_profile.test_scores
        for t in test_scores:
            if t.name == 'SAT':
                sat = max(sat, t.score) if sat != '––' else t.score
            if t.name == 'ACT':
                act = max(act, t.score) if act != '––' else t.score
        return render_template(
            'student/student_profile.html',
            user=current_user,
            sat=sat,
            act=act)


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
