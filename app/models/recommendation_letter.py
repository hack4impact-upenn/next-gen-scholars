from .. import db


class RecommendationLetter(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
	# name of reference
	name = db.Column(db.String, index=True)
	# category of reference, e.g. '12th grade Calculus teacher', '11th grade biology teacher'
	category = db.Column(db.String, index=True)
	# statuses include 'Submitted', 'Pending', 'Incomplete'
	status = db.Column(db.String, index=True)
