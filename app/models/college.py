from .. import db


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    @staticmethod
    def get_college_by_name(name):
        return College.query.filter_by(name=name).first()

    @staticmethod
    def insert_colleges():
        college_names = {
            'University of Pennsylvania',
            'Columbia University',
            'Stanford University',
            'Princeton University',
            'Harvard University',
            'Cornell University',
            'Yale University',
            'Brown University',
            'Dartmouth College',
            'New York University',
            'University of California, Berkeley',
            'University of California, Los Angelos',
            'University of Michigan',
            'Carnegie Mellon University',
            'John Hopkins University',
            'University of Chicago',
            'Amherst College',
            'Williams College',
            'Massachusetts Institute of Technology',
            'Georgia Institute of Technology',
            'California Institute of Technology'
            'Duke University'
        }

        for c in college_names:
            college = College.get_college_by_name(c)
            if college is None:
                college = College(name=c)
            db.session.add(college)
        db.session.commit()

    def __repr__(self):
        return '<College: {}>'.format(self.name)
