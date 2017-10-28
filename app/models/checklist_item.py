from .. import db
from faker import Faker
import random


class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee = db.relationship('User')
    deadline = db.Column(db.Date, index=True) 
    text = db.Column(db.Text, index=True) 
    is_checked = db.Column(db.Boolean, index=True, default=False)
    # creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def generate_fake(count=2):
        fake = Faker()
        checklist_item = random.sample([
            'Write my essay',
            'Submit common app',
            'Update my essay',
            'Turn in FAFSA',
        ], count)
        checklist_items = []
        for i in range(count):
            checklist_items.append(ChecklistItem(
                text=checklist_item[i],
            ))
        return checklist_items

    def __repr__(self):
        return '<ChecklistItem {}, {}>'.format(self.assignee_id, self.text)