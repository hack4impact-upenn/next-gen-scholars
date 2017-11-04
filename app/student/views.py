from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from . import student
from .forms import (EditCollegeForm, EditEssayForm, EditTestScoreForm, EditCommonAppForm)
from ..models import (User, College, Essay, TestScore)
from .. import db

@student.route('/checklist')
@login_required
def checklist():
    """Counselor dashboard page."""
    return render_template('student/checklist.html')


@student.route('/profile')
@login_required
def view_user_profile():
	return render_template('student/student_profile.html', user = current_user)

@student.route('/profile/college/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_college(item_id):
    college = College.query.filter_by(id=item_id).first()
    if college:
        form = EditCollegeForm(college_name=college.name)
        if form.validate_on_submit():
            college.name=form.college_name.data
            db.session.add(college)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template('student/edit_profile_info.html', form=form)
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))


@student.route('/profile/test_score/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_test_score(item_id):
    test_score = TestScore.query.filter_by(id=item_id).first()
    if test_score:
        form = EditTestScoreForm(test_name=test_score.name, month=test_score.month, year=test_score.year, score=test_score.score)
        if form.validate_on_submit():
            test_score.name=form.test_name.data
            test_score.month=form.month.data
            test_score.year=form.year.data
            test_score.score=form.score.data
            db.session.add(test_score)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template('student/edit_profile_info.html', form=form)
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))


@student.route('/profile/essay/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_essay(item_id):
    essay = Essay.query.filter_by(id=item_id).first()
    if essay:
        form = EditEssayForm(essay_name=essay.name, link=essay.link)
        if form.validate_on_submit():
            essay.name=form.essay_name.data
            essay.link=form.link.data
            db.session.add(essay)
            db.session.commit()
            return redirect(url_for('student.view_user_profile'))
        return render_template('student/edit_profile_info.html', form=form)
    flash('Item could not be updated', 'error')
    return redirect(url_for('student.view_user_profile'))

@student.route('/profile/common_app_essay/edit', methods=['GET', 'POST'])
@login_required
def edit_common_app_essay():
    form = EditCommonAppForm(link=current_user.student_profile.common_app_essay)
    if form.validate_on_submit():
        current_user.student_profile.common_app_essay=form.link.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))
    return render_template('student/edit_profile_info.html', form=form)


@student.route('/profile/test_score/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_test_score(item_id):
    test_score = TestScore.query.filter_by(id=item_id).first()
    if test_score:
        db.session.delete(test_score)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))
    flash('Item could not be deleted', 'error')
    return redirect(url_for('student.view_user_profile'))


@student.route('/profile/essay/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_essay(item_id):
    essay = Essay.query.filter_by(id=item_id).first()
    if essay:
        db.session.delete(essay)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))
    flash('Item could not be deleted', 'error')
    return redirect(url_for('student.view_user_profile'))


@student.route('/profile/common_app_essay/delete', methods=['GET', 'POST'])
@login_required
def delete_common_app_essay():
    current_user.student_profile.common_app_essay=''
    db.session.add(current_user)
    db.session.commit()
    return redirect(url_for('student.view_user_profile'))


@student.route('/profile/college/delete/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_college(item_id):
    college = College.query.filter_by(id=item_id).first()
    if college:
        db.session.delete(college)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))
    flash('Item could not be deleted', 'error')
    return redirect(url_for('student.view_user_profile'))
