from .. import db


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # PERSONAL INFO
    high_school = db.column(db.String, index=True)
    district = db.column(db.String, index=True)
    city = db.column(db.String, index=True)
    state = db.column(db.String(2), index=True)
    graduation_year = db.column(db.Integer(4), index=True)
    grade = db.column(db.Integer(2), index=True)  
    # ACADEMIC INFO
    gpa = db.column(db.Float, index=True)
    test_scores = db.relationship('TestScore', backref='student_profile', lazy=True, index=True)
    majors = db.relationship('Major', secondary='majors', lazy='subquery',
        backref=db.backref('student_profiles', lazy=True), index=True)
    colleges = db.relationship('College', secondary='colleges', lazy='subquery',
        backref=db.backref('student_profiles', lazy=True), index=True)
    # APPLICATION INFO
    common_app_essay = db.Column(db.String, index=True)
    essays = db.relationship('Essay', backref='student_profile', lazy=True, index=True)
    recommendation_letters = db.relationship('RecommendationLetter', backref='student_profile', lazy=True, index=True)