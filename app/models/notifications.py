from .. import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
