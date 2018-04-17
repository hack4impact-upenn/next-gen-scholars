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

    @staticmethod
    def generate_fake():
        alerts = [None] * 5
        alerts[0] = SMSAlert(
            title='UPenn Deadline Reminder',
            content=
            'Make sure to submit your application to the University of Pennsylvania by next Friday, 11:59PM!',
            date=datetime.date(2017, 12, 29),
            time=datetime.time(12, 0))
        alerts[1] = SMSAlert(
            title='Common App Deadline Reminder',
            content=
            'Merry Christmas everyone! Just a friendly reminder to make sure you submit your college application through the CommonApp portal by January 1st, 11:59PM!',
            date=datetime.date(2017, 12, 25),
            time=datetime.time(9, 0))
        alerts[2] = SMSAlert(
            title='UC Essay Workshop',
            content=
            'Come in to our office this Thursday at 3PM for a college app writing workshop!',
            date=datetime.date(2017, 11, 30),
            time=datetime.time(16, 0))
        alerts[3] = SMSAlert(
            title='Send SAT Scores (1 month before)',
            content=
            'Remember to send your SAT scores to colleges you\'re interested in! They must be sent by next month.',
            date=datetime.date(2017, 10, 15),
            time=datetime.time(12, 0))
        alerts[4] = SMSAlert(
            title='Send SAT Scores (1 week before)',
            content=
            'Remember to send your SAT scores to colleges you\'re interested in! They must be sent by next week.',
            date=datetime.date(2017, 11, 4),
            time=datetime.time(12, 0))
        for alert in alerts:
            db.session.add(alert)
            db.session.commit()
