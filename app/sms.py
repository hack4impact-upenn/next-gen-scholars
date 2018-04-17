import os

from flask import render_template
from flask_mail import Message
from datetime import datetime, timedelta
from twilio.rest import Client
import re

from app import create_app, db
from app.models import SMSAlert, User


def format_phone(number):
    return '+1' + re.sub('[^0-9]', '', number) if number[0] != '+' else number


def next_timestamp(dt):
    """
    Given a datetime dt, return the next quarter of an hour.
    Ex: 4:35:32 pm --> 4:45:00 pm, 1:00:00am --> 1:00:00am, etc.
    """
    if dt.minute % 15 or dt.second:
        return dt + timedelta(minutes=15 - dt.minute % 15,
                              seconds=-(dt.second % 60))
    return dt


def check_alerts():
    """
    Calls send_alert for each SMSAlert that should be sent within the next 15 minutes.
    """
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():
        next = next_timestamp(datetime.now())
        alerts = []
        for alert in SMSAlert.query.filter_by(date=next.date()).all():
            if not alert.sent and alert.time.hour == next.hour and alert.time.minute == next.minute:
                alerts.append(alert)
        students = User.query.filter(User.student_profile_id != None).filter(
            User.phone_number != None).all()

        account_sid = os.environ.get('TWILIO_ACCOUNT_SID') or None
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN') or None
        twilio_phone = os.environ.get('TWILIO_PHONE_NO') or None

        if not account_sid or not auth_token or not twilio_phone:
            print('Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NO to config.env file')
            return

        client = Client(account_sid, auth_token)

        for alert in alerts:
            for student in students:
                client.messages.create(to=format_phone(student.phone_number),
                                       from_=twilio_phone,
                                       body=alert.content)
            alert.sent = True
            db.session.add(alert)
        db.session.commit()
