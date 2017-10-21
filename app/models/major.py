from .. import db


class Major(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, index=True)