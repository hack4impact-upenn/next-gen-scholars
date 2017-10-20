from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager

class TestScore(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64), index = True) 
    score = db.Column(db.Integer(100), index = True) 
    month = db.Column(db.String(15), index = True) 
    year = db.Column(db.Integer(4), index = True) 

