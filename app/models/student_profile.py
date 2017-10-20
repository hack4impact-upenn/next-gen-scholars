from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager

class StudentProfile(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    colleges = db.Column(db.String(10000), index = True) 
    common_app_essay = db.Column(db.String(1000), index = True)
    college_essays = db.Column(db.Integer(10000), index = True) 
    recommendation_letters = db.Column(db.String(10000), index = True) 
    resume = db.column(db.String(10000), index = True)
    high_school = db.column(db.String(1000), index = True)
    state = db.column(db.String(1000), index = True)
    city = db.column(db.String(1000), index = True)
    district = db.column(db.String(1000), index = True)
    graduation_year = db.column(db.Integer(4), index = True)
    grade = db.column(db.Integer(2), index = True)
    majors = db.column(db.String(10000), index = True)





