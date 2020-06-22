from flask import render_template
from flask_login import login_required
from ..models import EditableHTML
from . import main

@main.route('/')
def index():
    editable_html_obj = EditableHTML.get_editable_html('index')
    return render_template(
        'main/index.html', editable_html_obj=editable_html_obj, pageType='home')
    return render_template('main/index.html', pageType='home')

@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)

@main.route('/calendar', methods=['GET', 'POST'])
def calendar():
    return render_template('main/calendar.html')

@main.route('/scattergram', methods=['GET', 'POST'])
@login_required
def scattergram():
    return render_template('main/scattergram.html')

@main.route('/comparer', methods=['GET', 'POST'])
@login_required
def comparer():
    return render_template('main/college_comparer.html')