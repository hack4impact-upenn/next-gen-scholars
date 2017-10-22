from .. import db


class Major(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    @staticmethod
    def get_major_by_name(name):
        return Major.query.filter_by(name=name.title()).first()

    @staticmethod
    def insert_majors():
        major_names = {
            'Accounting',
            'Agriculture',
            'Anthropology',
            'Architecture',
            'Art History',
            'Biochemistry',
            'Bioengineering',
            'Biology',
            'Business Administration and Management',
            'Chemistry',
            'Civil Engineering',
            'Computer Science',
            'Economics',
            'English',
            'Finance',
            'Gender Studies',
            'History',
            'Journalism',
            'Marketing',
            'Mathematics',
            'Mechanical Engineering',
            'Media Studies',
            'Music',
            'Nursing',
            'Philosophy',
            'Physics',
            'Political Science',
            'Psychology',
            'Public Relations',
            'Sociology',
            'Statistics',
            'Theater'
        }
        for m in major_names:
            major = Major.get_major_by_name(m)
            if major is None:
                major = Major(name=m)
            db.session.add(major)
        db.session.commit()

    def __repr__(self):
        return '<Major: {}>'.format(self.name)
