import random
from faker import Faker
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
    def generate_fake(count=3):
        test_types = [
            {'name': 'SAT', 'max_score': 2400},
            {'name': 'ACT', 'max_score': 36},
            {'name': 'SAT Literature', 'max_score': 800},
            {'name': 'SAT US History', 'max_score': 800},
            {'name': 'SAT World History', 'max_score': 800},
            {'name': 'SAT Biology', 'max_score': 800},
            {'name': 'SAT Physics', 'max_score': 800},
            {'name': 'SAT Chemistry', 'max_score': 800},
            {'name': 'SAT Mathematics', 'max_score': 800},
        ]
        years = ['2017', '2016', '2015', '2014']
        test_scores = []
        for _ in range(count):
            fake = Faker()
            test = random.choice(test_types)
            test_score = TestScore(
                # student_profile_id=student_profile.id,
                name=test['name'],
                score=random.randint(
                    (test['max_score'] * 0.75), test['max_score']) // 10 * 10,
                month=fake.month_name(),
                year=random.choice(years)
            )
            test_scores += [test_score]
        return test_scores

    def __repr__(self):
        return '<TestScore {}, {}, {} {}>'.format(self.name, self.score, self.month, self.year)
