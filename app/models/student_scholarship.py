import random
from faker import Faker
from .. import db
from sqlalchemy.orm import validates

class StudentScholarship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(
        db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    # college name
    name = db.Column(db.String, index=True)
    # statuses include 'Accepted', 'Accepted with award letter', 'Pending Award Letter Parsing'
    award_amount = db.Column(db.Float, index=True)

    @staticmethod
    def generate_fake(count=2):
        fake = Faker()
        names = random.sample([
            'Boatwright',
            'Bonner Scholarship',
            'Bright Futures',
            'Richmond Scholar',
        ], count)
        awards = random.sample([
            200,
            400,
            600,
            800
        ], count)
        schol = []
        for i in range(count):
            schol.append(
                StudentScholarship(
                    name=names[i],
                    award_amount=awards[i]))
        return schol

    def __repr__(self):
        return '<Student Scholarship {}, {}>'.format(self.name, self.award_amount)
