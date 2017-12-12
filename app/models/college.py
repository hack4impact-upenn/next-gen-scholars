from .. import db

import random
from datetime import datetime


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.String, index=True)
    regular_deadline = db.Column(db.Date, index=True)
    early_deadline = db.Column(db.Date, index=True)

    @staticmethod
    def get_college_by_name(name):
        return College.query.filter_by(name=name).first()

    @staticmethod
    def insert_colleges():
        college_names = {
            'University of Pennsylvania', 'Columbia University',
            'Stanford University', 'Princeton University',
            'Harvard University', 'Cornell University', 'Yale University',
            'Brown University', 'Dartmouth College', 'New York University',
            'University of California, Berkeley',
            'University of California, Los Angelos', 'University of Michigan',
            'Carnegie Mellon University', 'John Hopkins University',
            'University of Chicago', 'Amherst College', 'Williams College',
            'Massachusetts Institute of Technology',
            'Georgia Institute of Technology',
            'California Institute of Technology', 'Duke University'
        }
        early_deadlines = [
            datetime(2017, 11, 4),
            datetime(2017, 11, 3),
            datetime(2017, 10, 26),
            datetime(2017, 11, 1),
            datetime(2017, 11, 11),
            datetime(2017, 11, 13),
            datetime(2017, 10, 29)
        ]
        regular_deadlines = [
            datetime(2017, 12, 31),
            datetime(2017, 1, 1),
            datetime(2017, 1, 2),
            datetime(2017, 1, 3),
            datetime(2017, 1, 5),
            datetime(2017, 2, 1),
            datetime(2017, 1, 14)
        ]
        descriptions = [
            'Private research university',
            'Ivy League university',
            'Liberal arts college',
            'Public research university',
            'Private doctorate university'
        ]

        for c in college_names:
            college = College.get_college_by_name(c)
            if college is None:
                college = College(name=c, description=random.choice(descriptions),
                                  regular_deadline=random.choice(
                                      regular_deadlines),
                                  early_deadline=random.choice(early_deadlines))
            db.session.add(college)
        db.session.commit()

    def __repr__(self):
        return '<College: {}>'.format(self.name)
