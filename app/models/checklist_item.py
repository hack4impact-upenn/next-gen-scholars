from .. import db


class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee = db.relationship('User')
    deadline = db.Column(db.Date, index=True) 
    text = db.Column(db.Text, index=True) 
    is_checked = db.Column(db.Boolean, index=True, default=False)
    # creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)