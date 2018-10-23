from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
import os
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, index=True)
    hash_pass = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    profile_pic_path = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    # comments = db.relationship('Comment', backref='user', lazy='dynamic')
    # upvotes = db.relationship('UpVote', backref='user', lazy='dynamic')
    # downvotes = db.relationship('DownVote', backref='user', lazy='dynamic')
    # photos = db.relationship('PhotoProfile', backref='user', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError("You cannot read password attribute")

    @password.setter
    def password(self, password):
        self.hash_pass = generate_password_hash(password)

    def set_password(self, password):
        self.hash_pass = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hash_pass, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, os.environ.get('SECRET_KEY'),
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password(token):
        try:
            id = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'
