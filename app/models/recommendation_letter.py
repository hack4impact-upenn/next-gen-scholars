import random
from faker import Faker
from .. import db


class RecommendationLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(db.Integer, db.ForeignKey(
        'student_profile.id'), nullable=False)
    # name of reference
    name = db.Column(db.String, index=True)
    # category of reference, e.g. '12th grade Calculus teacher', '11th grade biology teacher'
    category = db.Column(db.String, index=True)
    # statuses include 'Submitted', 'Pending', 'Incomplete'
    status = db.Column(db.String, index=True)

    @staticmethod
    def generate_fake(count=2):
        fake = Faker()
        categories = random.sample([
            '12th grade Calculus teacher',
            '12th grade physics teacher',
            '11th grade biology teacher',
            '11th grade chemistry teacher',
            '11th grade music teacher',
            '11th grade English teacher',
            '10th grade history teacher',
            'High school principal',
            'Employer',
        ], count)
        statuses = ['Submitted', 'Pending', 'Incomplete']
        rec_letters = []
        for i in range(count):
            rec_letters.append(RecommendationLetter(
                name=fake.name(),
                category=categories[i],
                status=random.choice(statuses)
            ))
        return rec_letters

    def __repr__(self):
        return '<RecommendationLetter {}, {}, {}>'.format(self.name, self.category, self.status)
