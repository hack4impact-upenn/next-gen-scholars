from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
from .forms import (
    AddTestScoreForm, AddRecommendationLetterForm, AddEssayForm)
from ..models import TestScore, RecommendationLetter, Essay
from .. import db
from . import student


@student.route('/checklist')
@login_required
def checklist():
    """Counselor dashboard page."""
    return render_template('student/checklist.html')


@student.route('/profile')
@login_required
def view_user_profile():
    sat = '––'
    act = '––'
    student_profile = current_user.student_profile
    if student_profile is not None:
        test_scores = student_profile.test_scores
        for t in test_scores:
            if t.name == 'SAT':
                sat = t.score
            if t.name == 'ACT':
                act = t.score
        return render_template('student/student_profile.html', user=current_user, sat=sat, act=act)


@student.route('/profile/add_test_score', methods=['GET', 'POST'])
@login_required
def add_test_score():
    # display list of default checklist items and option to add a new one
    form = AddTestScoreForm()
    if form.validate_on_submit():
        # create new test score from form data
        new_item = TestScore(
            student_profile_id=current_user.student_profile_id,
            name=form.test_name.data,
            score=form.test_score.data,
            month=form.test_month.data,
            year=form.test_year.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))

    return render_template('student/add_test_score.html', form=form)


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

    return render_template('student/add_recommendation_letter.html', form=form)


@student.route('/profile/add_essay', methods=['GET', 'POST'])
@login_required
def add_essay():
    # display list of default checklist items and option to add a new one
    form = AddEssayForm()
    if form.validate_on_submit():
        # create new test score from form data
        new_item = Essay(
            student_profile_id=current_user.student_profile_id,
            name=form.name.data,
            link=form.link.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('student.view_user_profile'))

    return render_template('student/add_essay.html', form=form)
