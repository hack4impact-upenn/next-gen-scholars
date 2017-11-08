import random
from faker import Faker
from . import College, Essay, Major, RecommendationLetter, TestScore, ChecklistItem
from .. import db


student_colleges = db.Table('student_colleges',
                            db.Column('college_id', db.Integer,
                                      db.ForeignKey('college.id')),
                            db.Column('student_profile_id', db.Integer,
                                      db.ForeignKey('student_profile.id'))
                            )

student_majors = db.Table('student_majors',
                          db.Column('major_id', db.Integer,
                                    db.ForeignKey('major.id')),
                          db.Column('student_profile_id', db.Integer,
                                    db.ForeignKey('student_profile.id'))
                          )


class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship("User", back_populates="student_profile")
    # PERSONAL INFO
    high_school = db.Column(db.String, index=True)
    district = db.Column(db.String, index=True)
    city = db.Column(db.String, index=True)
    state = db.Column(db.String, index=True)
    graduation_year = db.Column(db.String, index=True)
    grade = db.Column(db.Integer, index=True)
    # ACADEMIC INFO
    gpa = db.Column(db.Float, index=True)
    test_scores = db.relationship(
        'TestScore', backref='student_profile', lazy=True)
    majors = db.relationship('Major', secondary=student_majors,
                             backref=db.backref('student_profiles', lazy='dynamic'))
    colleges = db.relationship('College', secondary=student_colleges,
                               backref=db.backref('student_profiles', lazy='dynamic'))
    # APPLICATION INFO
    fafsa_completed = db.Column(db.Boolean, index=True, default=False)
    common_app_essay = db.Column(db.String, index=True) # link to common app essay
    essays = db.relationship('Essay')
    recommendation_letters = db.relationship('RecommendationLetter')
    checklist = db.relationship('ChecklistItem')

    @staticmethod
    def generate_fake():
        fake = Faker()
        year = random.choice([['2018', '12'], ['2019', '11'], ['2020', '10']])
        profile = StudentProfile(
            high_school='{} High School'.format(fake.street_name()),
            district='{} District'.format(fake.city()),
            city=fake.city(),
            state=fake.state(),
            graduation_year=year[0],
            grade=year[1],
            gpa=round(random.uniform(2, 4), 2),
            test_scores=TestScore.generate_fake(),
            majors=random.sample(Major.query.all(), 3),
            colleges=random.sample(College.query.all(), 3),
            common_app_essay='https://google.com',
            essays=Essay.generate_fake(),
            recommendation_letters=RecommendationLetter.generate_fake(),
            checklist = ChecklistItem.generate_fake()
        )
        return profile

    def __repr__(self):
        s = '<Student Profile\n'
        s += 'High School: {}\n'.format(self.high_school)
        s += 'District: {}\n'.format(self.district)
        s += 'City, State: {}, {}\n'.format(self.city, self.state)
        s += 'Gradution Year: {}\n'.format(self.graduation_year)
        s += 'Grade: {}\n'.format(self.grade)
        s += 'GPA: {}\n'.format(self.gpa)
        s += 'Test Scores: {}\n'.format(self.test_scores)
        s += 'Majors: {}\n'.format(','.join([m.name for m in self.majors]))
        s += 'Colleges: {}\n'.format(','.join([c.name for c in self.colleges]))
        s += 'Common App Essay: {}\n'.format(self.common_app_essay)
        s += 'Essays: {}\n'.format(self.essays)
        s += 'Recommendation Letters: {}'.format(
            self.recommendation_letters) + '>'
        return s
