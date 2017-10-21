from .. import db


majors = db.Table('majors',
	db.Column('major_id', db.Integer, db.ForeignKey('major_id')),
	db.Column('student_profile_id', db.Integer, db.ForeignKey('student_profile.id'))
)


class Major(db.Model):
	__tablename__ = "majors"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, index=True)