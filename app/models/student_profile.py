from .. import db


student_colleges = db.Table('student_colleges',
    db.Column('college_id', db.Integer, db.ForeignKey('college.id')),
    db.Column('student_profile_id', db.Integer, db.ForeignKey('student_profile.id'))
)

student_majors = db.Table('student_majors',
    db.Column('major_id', db.Integer, db.ForeignKey('major.id')),
    db.Column('student_profile_id', db.Integer, db.ForeignKey('student_profile.id'))
)


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="student_profile")
    # PERSONAL INFO
    high_school = db.Column(db.String, index=True)
    district = db.Column(db.String, index=True)
    city = db.Column(db.String, index=True)
    state = db.Column(db.String(2), index=True)
    graduation_year = db.Column(db.Integer, index=True)
    grade = db.Column(db.Integer, index=True)  
    # ACADEMIC INFO
    gpa = db.Column(db.Float, index=True)
    test_scores = db.relationship('TestScore', backref='student_profile', lazy=True)
    majors = db.relationship('Major', secondary=student_majors,
        backref=db.backref('student_profiles', lazy='dynamic'))
    colleges = db.relationship('College', secondary=student_colleges, 
        backref=db.backref('student_profiles', lazy='dynamic'))
    # APPLICATION INFO
    common_app_essay = db.Column(db.String, index=True)
    essays = db.relationship('Essay', backref='student_profile', lazy=True)
    recommendation_letters = db.relationship('RecommendationLetter', backref='student_profile', lazy=True)