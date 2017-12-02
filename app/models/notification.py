import datetime
from .. import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    student_profile_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    seen = db.Column(db.Boolean, default=False)

    @staticmethod
    def get_user_notifications(student_profile_id):
        return Notification.query.filter_by(
            student_profile_id=student_profile_id).all()
