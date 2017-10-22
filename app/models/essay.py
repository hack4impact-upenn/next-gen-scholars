import random
from .. import db


class Essay(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    student_profile_id = db.Column(
        db.Integer,
        db.ForeignKey('student_profile.id'),
        nullable=False,
        index=True
    )
    link = db.Column(db.String, index=True)

    @staticmethod
    def generate_fake_essay(student_profile):
        essay_names = {
            'UPenn Why Essay',
            'Dartmouth Supplemental Essay',
            'Columbia Why Essay',
            'Cornell Engineering Essay',
            'NYU Business Why Essay',
            'M&T Supplemental',
            'Vagelos Supplemental',
            'MIT Activity Essay',
            'UChicago Community Supplemental',
            'Harvard Why Essay'
        }
        essay = Essay(
            name=random.choice(essay_names),
            student_profile_id=student_profile.id
        )
        return essay
