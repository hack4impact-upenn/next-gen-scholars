from .. import db


colleges = db.Table('colleges',
	db.Column('college_id', db.Integer, db.ForeignKey('college_id')),
	db.Column('student_profile_id', db.Integer, db.ForeignKey('student_profile.id'))
)


class College(db.Model):
	__tablename__ = "colleges"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, index=True)