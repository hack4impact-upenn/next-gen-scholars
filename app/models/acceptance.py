import random
from faker import Faker
from .. import db
from sqlalchemy.orm import validates

class Acceptance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(
        db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    # college name
    college = db.Column(db.String, index=True)
    # statuses include 'Accepted', 'Accepted with award letter', 'Pending Award Letter Parsing'
    status = db.Column(db.String, index=True)
    link = db.Column(db.String, index=True)

    @validates('status')
    def validate_status(self, key, status):
        assert status in ['Accepted with award letter', 'Accepted', 'Pending Award Letter Parsing'
        ]
        return status

    @staticmethod
    def generate_fake(count=2):
        fake = Faker()
        names = random.sample([
            'Cornell',
            'Princeton',
            'University of Florida',
            'University of Richmond',
        ], count)
        statuses = [
            'Accepted', 'Accepted with award letter',
            'Pending Award Letter Parsing'
        ]
        acc = []
        for i in range(count):
            acc.append(
                Acceptance(
                    college=names[i],
                    status=random.choice(statuses),
                    link='https://google.com'))
        return acc

    def __repr__(self):
        return '<Acceptance {}, {}>'.format(self.name, self.status)
