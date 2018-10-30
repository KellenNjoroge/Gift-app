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
    photos = db.relationship('PhotoProfile', backref='user', lazy="dynamic")
    #coments = db.relationship('Comment', backref='user', lazy='dynamic')
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


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer, primary_key=True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Place(db.Model):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    place_content = db.Column(db.String())
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    place_pic = db.Column(db.String(255))
    photo_url = db.Column(db.String(500))
    location_url = db.Column(db.String(500))

    comment = db.relationship('Comment', backref='place', lazy='dynamic')
    photo = db.relationship('Photo', backref='place', lazy='dynamic')

    def save_place(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_places(cls):
        places = Place.query.order_by('-id').all()
        return places

    @classmethod
    def get_single_place(cls, id):
        place = Place.query.filter_by(id=id).first()
        return place


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    comment_content = db.Column(db.String())
    date_comment = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_place_comments(cls, id):
        comments = Comment.query.filter_by(place_id=id).order_by('-id').all()
        return comments

    @classmethod
    def get_single_comment(cls, id_place, id):
        comment = Comment.query.filter_by(place_id=id_place, id=id).first()
        return comment


class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_data = db.Column(db.String(255))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
