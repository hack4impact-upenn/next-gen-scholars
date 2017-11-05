from flask import url_for
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (StringField, IntegerField, SubmitField)
from wtforms.validators import Email, EqualTo, InputRequired, Length

class EditCommonAppEssayForm(Form):
    link = StringField(
        'Link to Common App Essay', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update essay link')

class EditCollegeForm(Form):
    college_name = StringField(
        'College Name', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update college name')

class EditTestScoreForm(Form):
    test_name = StringField(
        'Test Name', validators=[InputRequired(), Length(1, 64)])
    month = StringField(
        'Month', validators=[InputRequired(), Length(1, 64)])
    year = StringField(
        'Year', validators=[InputRequired(), Length(1, 64)])
    score = IntegerField(
        'Test Score', validators=[InputRequired()])
    submit = SubmitField('Update test score')

class EditSupplementalEssayForm(Form):
    essay_name = StringField(
        'Essay Name', validators=[InputRequired(), Length(1, 64)])
    link = StringField(
        'Essay Link', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update essay')

class AddChecklistItemForm(Form):
    item_text = StringField(
        'Checklist Item', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Add checklist item')

class EditChecklistItemForm(Form):
    item_text = StringField(
        'New text', validators=[InputRequired(), Length(1, 64)])
    submit = SubmitField('Update checklist item')