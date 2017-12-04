import datetime
from .. import db


class SMSAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    content = db.Column(db.String, index=True)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Time, index=True)

    def format_date(self):
        return self.date.strftime("%m/%d/%Y")

    def format_time(self):
        return self.time.strftime("%-I:%M %p")
