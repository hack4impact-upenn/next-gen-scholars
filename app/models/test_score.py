from .. import db


class TestScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'))
    name = db.Column(db.String, index = True) 
    score = db.Column(db.Integer, index = True)
    month = db.Column(db.String, index = True)
    year = db.Column(db.Integer, index = True)