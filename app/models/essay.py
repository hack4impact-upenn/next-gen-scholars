from .. import db


class Essay(db.Model):
	__tablename__ = "essays"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, index=True)
	student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False, index=True)
	link = db.Column(db.String, index=True)