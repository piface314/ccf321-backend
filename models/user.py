from db import db
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


class User(db.Model):

    __tablename__ = 'user'

    username = db.Column('username', db.VARCHAR(length=64), nullable=False, primary_key=True)
    password = db.Column('password', db.VARCHAR(length=64), nullable=False)

    @classmethod
    def get(cls, username):
        return cls.query.get(username)

    @classmethod
    def get_by_token(cls, token, key):
        try:
            data = jwt.decode(token, key, algorithms=['HS256'])
        except:
            return None, None
        return cls.query.get(data['username']), data['exp']

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def as_dict(self):
        return { 'username': self.username }

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, key, duration = 3600):
        return jwt.encode({
            'username': self.username,
            'exp': time() + duration
        }, key, algorithm='HS256')

    def add(self):
        db.session.add(self)
        db.session.commit()
