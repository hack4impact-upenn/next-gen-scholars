from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required
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
