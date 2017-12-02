from .. import db

class CollegeStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(db.Integer,
                                   db.ForeignKey('student_profile.id'))
    name = db.Column(db.String, index=True)
    status = db.Column(db.String, index = True)

    def __repr__(self):
        return '<CollegeStatus {}, {}>'.format(self.name, self.status)
