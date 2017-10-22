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
            'Carnegie Mellon University',
            'Columbia University',
            'Stanford University',
            'Massachusetts Institute of Technology',
            'Princeton University',
            'Dartmouth College',
            'University of California, Berkeley',
            'Amherst College',
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
