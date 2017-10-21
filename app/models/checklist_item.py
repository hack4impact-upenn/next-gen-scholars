from .. import db

class ChecklistItem(db.Model):
	__tablename__ = "checklist_items"
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'), nullable=False)
    deadline = db.Column(db.Date, index=True) 
    text = db.Column(db.Text, index=True) 
    checked = db.Column(db.Boolean, index=True, Default=False)
