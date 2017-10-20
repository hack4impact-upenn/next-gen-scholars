from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db, login_manager

class Checklist(db.Model):
    __tablename__ = 'checklist'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    deadline = db.Column(db.Date(50), index = True) 
    text = db.Column(db.String(10000), index = True) 
    checked = db.Column(db.Boolean(10), index = True, Default = False) 
 






