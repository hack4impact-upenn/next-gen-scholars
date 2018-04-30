from .. import db

class Interest(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	lvl = db.Column(db.String(10), index=True)
	name = db.Column(db.Integer, index=True)

	def __repr__(self):
		return '<Interest: {}>'.format(self.lvl)