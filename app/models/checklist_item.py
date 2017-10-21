from .. import db


class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    deadline = db.Column(db.Date, index=True) 
    text = db.Column(db.Text, index=True) 
    isChecked = db.Column(db.Boolean, index=True, default=False)
