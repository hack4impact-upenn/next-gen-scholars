import random
from .. import db


class TestScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(
        db.Integer, db.ForeignKey('student_profile.id'))
    name = db.Column(db.String, index=True)
    score = db.Column(db.Integer, index=True)
    month = db.Column(db.String, index=True)
    year = db.Column(db.String, index=True)

    @staticmethod
    def generate_fake_test_scores(student_profile, count=3):
        tests = {
            {name='SAT',max_score=2400},
            {name='ACT',max_score=36},
            {name='SAT Literature',max_score=800},
            {name='SAT US History',max_score=800},
            {name='SAT World History',max_score=800},
            {name='SAT Biology',max_score=800},
            {name='SAT Physics',max_score=800},
            {name='SAT Chemistry',max_score=800},
            {name='SAT Mathematics',max_score=800},
        }
        years = {'2017', '2016', '2015', '2014'}
        tests = []
        for _ in range(count):
            test = random.choice(tests)
            test_score = TestScore(
                student_profile_id=student_profile.id,
                name=test.name,
                score=randint(test.max_score * 0.75,test.max_score),
                month=fake.month_name(),
                year=random.choice(years)
            )
            tests += [test]
        return tests
