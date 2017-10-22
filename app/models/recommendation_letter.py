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
    def generate_fake_rec_letter(student_profile):
        categories = {
            '12th grade Calculus teacher',
            '12th grade physics teacher',
            '11th grade biology teacher',
            '11th grade chemistry teacher',
            '11th grade music teacher',
            '11th grade English teacher',
            '10th grade history teacher',
            'High school principal',
            'Employer',
        }
        statuses = {'Submitted', 'Pending', 'Incomplete'}
        rec_letter = RecommendationLetter(
            student_profile_id=student_profile.id
            name=faker.name(),
            category=random.choice(categories),
            status=random.choice(statuses)
        )
        retrun rec_letter
