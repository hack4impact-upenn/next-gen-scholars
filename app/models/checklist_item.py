from .. import db
from faker import Faker
import random


class ChecklistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignee_id = db.Column(
        db.Integer,
        db.ForeignKey('student_profile.id'),
        nullable=False,
        index=True)
    deadline = db.Column(db.Date, index=True)
    text = db.Column(db.Text, index=True)
    is_checked = db.Column(db.Boolean, index=True, default=False)
    is_deletable = db.Column(db.Boolean, index=True, default=False)
    creator_role_id = db.Column(db.Integer, index=True, default=1)
    is_default_item = db.Column(db.Boolean, index=True, default=False)
    cal_event_id = db.Column(db.Text, index=True)
    event_created = db.Column(db.Boolean, index=True)

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
            checklist_items.append(ChecklistItem(text=checklist_item[i], ))
        return checklist_items

    def __repr__(self):
        return '<ChecklistItem {}, {}>'.format(self.assignee_id, self.text)
